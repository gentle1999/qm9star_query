'''
Author: TMJ
Date: 2024-04-29 10:53:34
LastEditors: TMJ
LastEditTime: 2024-04-29 11:01:13
Description: 请填写简介
'''
from datetime import datetime
from typing import List

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlmodel import Field, SQLModel


class MoleculeBase(SQLModel):
    # Topological properties of the molecule
    smiles: str = Field(index=True, unique=True)
    total_charge: int
    total_multiplicity: int

    # Molecule properties
    qed: float | None = Field(default=None, nullable=True)
    logp: float | None = Field(default=None, nullable=True)

    # vectors
    morgan_fp3_1024: List[int] = Field(sa_column=Column(Vector(1024)))
    rdkit_fp_1024: List[int] = Field(sa_column=Column(Vector(1024)))
    atompair_fp_1024: List[int] = Field(sa_column=Column(Vector(1024)))
    topological_torsion_fp_1024: List[int] = Field(sa_column=Column(Vector(1024)))


class MoleculeCreate(MoleculeBase):
    smiles: str
    total_charge: int
    total_multiplicity: int
    qed: float | None = None
    logp: float | None = None
    morgan_fp3_1024: List[int] = Field(sa_column=Column(Vector(1024)))
    rdkit_fp_1024: List[int] = Field(sa_column=Column(Vector(1024)))
    atompair_fp_1024: List[int] = Field(sa_column=Column(Vector(1024)))
    topological_torsion_fp_1024: List[int] = Field(sa_column=Column(Vector(1024)))


class MoleculeUpdate(MoleculeCreate):
    update_time: datetime = Field(default_factory=datetime.now)