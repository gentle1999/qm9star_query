"""
Author: TMJ
Date: 2024-04-29 10:51:44
LastEditors: TMJ
LastEditTime: 2024-04-29 11:02:50
Description: 请填写简介
"""

from datetime import datetime

from qm9star_query.models.user import UserBase
from qm9star_query.models.formula import FormulaBase
from qm9star_query.models.molecule import MoleculeBase
from qm9star_query.models.snapshot import SnapshotBase
from sqlalchemy import ARRAY, Column, Integer
from sqlmodel import Field, Relationship


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

    snapshots: list["Snapshot"] = Relationship(back_populates="owner")


class Formula(FormulaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    commit_time: datetime = Field(default_factory=datetime.now)
    update_time: datetime = Field(default_factory=datetime.now)

    molecule_number: int = Field(default=0)
    molecule_ids: list[int] = Field(sa_column=Column(ARRAY(Integer)), default=[])
    molecules: list["Molecule"] = Relationship(back_populates="formula")


class Molecule(MoleculeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    commit_time: datetime = Field(default_factory=datetime.now)
    update_time: datetime = Field(default_factory=datetime.now)

    snapshot_number: int = Field(default=0)
    snapshot_ids: list[int] = Field(sa_column=Column(ARRAY(Integer)), default=[])
    snapshots: list["Snapshot"] = Relationship(back_populates="molecule")

    formula_id: int = Field(default=None, foreign_key="formula.id")
    formula: Formula = Relationship(back_populates="molecules")


class Snapshot(SnapshotBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hash_token: str | None = Field(default=None, unique=True, index=True)

    commit_time: datetime = Field(default_factory=datetime.now)
    update_time: datetime = Field(default_factory=datetime.now)

    owner_id: int = Field(default=None, foreign_key="user.id")
    owner: User = Relationship(back_populates="snapshots")

    molecule_id: int = Field(default=None, foreign_key="molecule.id")
    molecule: Molecule = Relationship(back_populates="snapshots")
