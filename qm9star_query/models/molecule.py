"""
Author: TMJ
Date: 2024-04-29 10:53:34
LastEditors: TMJ
LastEditTime: 2024-05-13 15:10:39
Description: 请填写简介
"""

from datetime import datetime
from typing import List

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlmodel import Field, SQLModel

from qm9star_query.models.formula import FormulaOut


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


class MoleculeOut(SQLModel):
    id: int
    smiles: str
    total_charge: int
    total_multiplicity: int
    qed: float | None = None
    logp: float | None = None

    formula: FormulaOut | None = None

    commit_time: datetime
    update_time: datetime


class MoleculeUpdate(MoleculeCreate):
    update_time: datetime = Field(default_factory=datetime.now)
