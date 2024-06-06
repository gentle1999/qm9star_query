"""
Author: TMJ
Date: 2024-05-06 15:46:57
LastEditors: TMJ
LastEditTime: 2024-05-07 10:43:34
Description: 请填写简介
"""

import os
from typing import Sequence, Union, Callable

import numpy as np
import torch
import torch.utils.data
from sqlmodel import Session, col, create_engine, func, select
from sqlmodel.sql.expression import SelectOfScalar
from torch import Tensor
from torch_geometric.data import Data, Dataset, InMemoryDataset
from torch_geometric.data.data import BaseData
from tqdm import tqdm

from qm9star_query.models import Formula, Snapshot
from qm9star_query.models.snapshot import SnapshotOut
from qm9star_query.utils import recover_rdmol

IndexType = Union[slice, Tensor, np.ndarray, Sequence]


def update_slices(slices_list):
    # 初始化一个全新的slices字典
    new_slices = {
        key: torch.zeros(1, dtype=torch.long) for key in slices_list[0].keys()
    }

    # 累积更新slices
    for slices in slices_list:
        for key in slices.keys():
            new_slices[key] = torch.cat(
                [new_slices[key], new_slices[key][-1] + slices[key][1:]]
            )

    return new_slices


def transform_data(raw_data: dict):
    return Data(
        pos=torch.tensor(raw_data["coords"], dtype=torch.float32),
        z=torch.tensor(raw_data["atoms"], dtype=torch.int64),
        energy=torch.tensor(raw_data["single_point_energy"], dtype=torch.float32),
        y=torch.tensor(raw_data["single_point_energy"], dtype=torch.float32),
        energy_grad=-torch.tensor(raw_data["forces"], dtype=torch.float32),
        formal_charges=torch.tensor(raw_data["formal_charges"], dtype=torch.int64),
        formal_num_radicals=torch.tensor(
            raw_data["formal_num_radicals"], dtype=torch.int64
        ),
        bonds=torch.tensor(raw_data["bonds"], dtype=torch.int64),
    )


class BaseQM9starDataset(InMemoryDataset):
    def __init__(
        self,
        root=os.path.curdir,
        user="hxchem",
        password="hxchem",
        server="127.0.0.1",
        port=5432,
        db="qm9star",
        dataset_name="qm9star_full",
        block_num=5,
        transform=transform_data,
        pre_transform=None,
        pre_filter=None,
        selector_func:Callable=None,
        log=False,
    ):
        self.dataset_name = dataset_name
        self.names = [f"{dataset_name}_chunk{i:02d}" for i in range(block_num)]
        self.session_url = (
            f"postgresql+psycopg2://{user}:{password}@{server}:{port}/{db}"
        )
        if selector_func:
            self.db_select = selector_func
        super().__init__(
            root,
            transform=transform,
            pre_transform=pre_transform,
            pre_filter=pre_filter,
            log=log,
        )
        data_lst = []
        slices_lst = []
        for processed_path in self.processed_paths:
            data, slices = torch.load(processed_path)
            data_lst.append(data)
            slices_lst.append(slices)
        self._data, _ = self.collate(data_lst)
        self.slices = update_slices(slices_lst)

    @property
    def raw_file_names(self) -> list[str]:
        return [f"{name}.npz" for name in self.names]

    @property
    def processed_file_names(self) -> list[str]:
        return [f"{name}_processed.pt" for name in self.names]

    def download(self) -> None:
        """
        Downloads the dataset from QM9star database to `raw` dir
        """
        self.check_session()
        for snapshot_ids, raw_path in zip(self.get_db_ids(), self.raw_paths):
            raw_data = self.get_data(
                snapshot_ids.tolist(), chunk_idx=self.raw_paths.index(raw_path)
            )
            np.savez(raw_path, data=raw_data)
            if self.log:
                print(f"{raw_path} saved")

    def check_session(self):
        """
        Checks if the session is valid
        """
        session = Session(create_engine(self.session_url))
        try:
            session.connection()
        except:
            raise Exception("Failed to connect to database")
        else:
            self.session = session

    def get_db_ids(self) -> list[np.ndarray]:
        self.db_ids = np.array_split(
            self.session.exec(
                self.db_select(select(Snapshot.id)).order_by(Snapshot.id)
            ).all(),
            len(self.names),
        )
        return self.db_ids

    def get_data(self, snapshot_ids: list[int], chunk_idx):
        if self.session is None:
            raise Exception("Session is None")
        return [
            SnapshotOut.model_validate(snapshot).model_dump()
            for snapshot in tqdm(
                self.session.exec(
                    self.db_select(select(Snapshot))
                    .where(col(Snapshot.id).in_(snapshot_ids))
                    .order_by(Snapshot.id)
                ).all(),
                desc=f"Downloading data {self.dataset_name} chunk {chunk_idx:02d}",
            )
        ]

    def process(self) -> None:
        for idx, raw_path in enumerate(self.raw_paths):
            if self.log:
                print(f"processing {self.processed_paths[idx]}")
            data_list = np.load(raw_path, allow_pickle=True)["data"]
            data, slices = self.collate([self.transform(data) for data in data_list])
            torch.save(
                (data, slices),
                self.processed_paths[idx],
            )
            if self.log:
                print(f"{self.processed_paths[idx]} saved")

    @staticmethod
    def db_select(
        selector=select(Snapshot),
    ) -> SelectOfScalar[int] | SelectOfScalar[Snapshot]:
        return selector

    def get_rdmol(self, index: int):
        data = self[index]
        return recover_rdmol(
            coords=np.array(data["pos"]).tolist(),
            atoms=np.array(data["z"]).tolist(),
            bonds=np.array(data["bonds"]).tolist(),
            formal_charges=np.array(data["formal_charges"]).tolist(),
            formal_num_radicals=np.array(data["formal_num_radicals"]).tolist(),
        )

    def __getitem__(
        self,
        idx: Union[int, np.integer, IndexType],
    ) -> Union["Dataset", BaseData]:
        r"""In case :obj:`idx` is of type integer, will return the data object
        at index :obj:`idx` (and transforms it in case :obj:`transform` is
        present).
        In case :obj:`idx` is a slicing object, *e.g.*, :obj:`[2:5]`, a list, a
        tuple, or a :obj:`torch.Tensor` or :obj:`np.ndarray` of type long or
        bool, will return a subset of the dataset at the specified indices.
        """
        if (
            isinstance(idx, (int, np.integer))
            or (isinstance(idx, Tensor) and idx.dim() == 0)
            or (isinstance(idx, np.ndarray) and np.isscalar(idx))
        ):

            data = self.get(self.indices()[idx])
            return data

        else:
            return self.index_select(idx)
