"""
Author: TMJ
Date: 2024-05-06 15:45:45
LastEditors: TMJ
LastEditTime: 2024-05-06 18:48:05
Description: 请填写简介
"""

import os

from sqlmodel import Session, create_engine, func, select
from sqlmodel.sql.expression import SelectOfScalar
from torch_geometric.data import Data
from tqdm import tqdm

from qm9star_query.dataset.base_dataset import BaseQM9starDataset, transform_data
from qm9star_query.models import Formula, Molecule, Snapshot


class NeutralQM9starDataset(BaseQM9starDataset):
    def __init__(
        self,
        root=os.path.curdir,
        user="hxchem",
        password="hxchem",
        server="127.0.0.1",
        port=5432,
        db="qm9star",
        dataset_name="qm9star_neutral",
        block_num=5,
        transform=transform_data,
        pre_transform=None,
        pre_filter=None,
        log=False,
    ):
        super().__init__(
            root=root,
            user=user,
            password=password,
            server=server,
            port=port,
            db=db,
            dataset_name=dataset_name,
            block_num=block_num,
            transform=transform,
            pre_transform=pre_transform,
            pre_filter=pre_filter,
            log=log,
        )

    def db_select(
        self, selector=select(Snapshot)
    ) -> SelectOfScalar[int] | SelectOfScalar[Snapshot]:
        return (
            selector.join(Molecule)
            .where(Molecule.total_charge == 0)
            .where(Molecule.total_multiplicity == 1)
        )


class CationQM9starDataset(BaseQM9starDataset):
    def __init__(
        self,
        root=os.path.curdir,
        user="hxchem",
        password="hxchem",
        server="127.0.0.1",
        port=5432,
        db="qm9star",
        dataset_name="qm9star_cation",
        block_num=5,
        transform=transform_data,
        pre_transform=None,
        pre_filter=None,
        log=False,
    ):
        super().__init__(
            root=root,
            user=user,
            password=password,
            server=server,
            port=port,
            db=db,
            dataset_name=dataset_name,
            block_num=block_num,
            transform=transform,
            pre_transform=pre_transform,
            pre_filter=pre_filter,
            log=log,
        )

    def db_select(
        self, selector=select(Snapshot)
    ) -> SelectOfScalar[int] | SelectOfScalar[Snapshot]:
        return (
            selector.join(Molecule)
            .where(Molecule.total_charge == 1)
            .where(Molecule.total_multiplicity == 1)
        )


class AnionQM9starDataset(BaseQM9starDataset):
    def __init__(
        self,
        root=os.path.curdir,
        user="hxchem",
        password="hxchem",
        server="127.0.0.1",
        port=5432,
        db="qm9star",
        dataset_name="qm9star_anion",
        block_num=5,
        transform=transform_data,
        pre_transform=None,
        pre_filter=None,
        log=False,
    ):
        super().__init__(
            root=root,
            user=user,
            password=password,
            server=server,
            port=port,
            db=db,
            dataset_name=dataset_name,
            block_num=block_num,
            transform=transform,
            pre_transform=pre_transform,
            pre_filter=pre_filter,
            log=log,
        )

    def db_select(
        self, selector=select(Snapshot)
    ) -> SelectOfScalar[int] | SelectOfScalar[Snapshot]:
        return (
            selector.join(Molecule)
            .where(Molecule.total_charge == -1)
            .where(Molecule.total_multiplicity == 1)
        )


class RadicalQM9starDataset(BaseQM9starDataset):
    def __init__(
        self,
        root=os.path.curdir,
        user="hxchem",
        password="hxchem",
        server="127.0.0.1",
        port=5432,
        db="qm9star",
        dataset_name="qm9star_radical",
        block_num=5,
        transform=transform_data,
        pre_transform=None,
        pre_filter=None,
        log=False,
    ):
        super().__init__(
            root=root,
            user=user,
            password=password,
            server=server,
            port=port,
            db=db,
            dataset_name=dataset_name,
            block_num=block_num,
            transform=transform,
            pre_transform=pre_transform,
            pre_filter=pre_filter,
            log=log,
        )

    def db_select(
        self, selector=select(Snapshot)
    ) -> SelectOfScalar[int] | SelectOfScalar[Snapshot]:
        return (
            selector.join(Molecule)
            .where(Molecule.total_charge == 0)
            .where(Molecule.total_multiplicity == 2)
        )
