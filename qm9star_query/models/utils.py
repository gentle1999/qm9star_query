"""
Author: TMJ
Date: 2024-04-29 14:44:01
LastEditors: TMJ
LastEditTime: 2024-04-29 14:45:46
Description: 请填写简介
"""

from datetime import datetime
from typing import List, Literal

from sqlmodel import Field, SQLModel


class NumericFilter(SQLModel):
    column: str
    min: float = float("-inf")
    max: float = float("inf")


class ElementFilter(SQLModel):
    element: str = Field(description="element symbol")
    count: int = Field(
        default=0, description="-1 for existing, 0 for non-existing, >0 for count"
    )


class FormulaFilter(SQLModel):
    numeric_filters: List[NumericFilter]
    element_filters: List[ElementFilter]


class MoleculeFilter(SQLModel):
    smiles: str = Field(description="SMILES string", default=None)
    method: Literal["morgan", "rdk", "atompair", "torsion"] = "morgan"
    distance: Literal["l2", "inner_product", "cosine"] = "cosine"
    numeric_filters: List[NumericFilter]
    element_filters: List[ElementFilter]


class ClassFilter(SQLModel):
    column: str
    values: List[str]


class BoolFilter(SQLModel):
    column: Literal["is_TS", "is_optimized", "is_error"]
    value: bool


class DateFilter(SQLModel):
    column: str
    min: datetime = datetime.min
    max: datetime = datetime.max


class SnapshotFilter(SQLModel):
    numeric_filters: List[NumericFilter]
    class_filters: List[ClassFilter]
    bool_filters: List[BoolFilter]
    element_filters: List[ElementFilter]
    smiles: str = Field(description="SMILES string", default=None)
    method: Literal["morgan", "rdk", "atompair", "torsion"] = "morgan"
    distance: Literal["l2", "inner_product", "cosine"] = "cosine"


class ItemCount(SQLModel):
    count: int
