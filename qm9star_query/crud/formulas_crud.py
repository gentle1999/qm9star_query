"""
Author: TMJ
Date: 2024-04-29 14:43:13
LastEditors: TMJ
LastEditTime: 2024-04-29 14:44:55
Description: 请填写简介
"""

from typing import Sequence

from sqlmodel import Session, select, func

from qm9star_query.models import Formula
from qm9star_query.models.utils import FormulaFilter, ItemCount
from qm9star_query.utils import elements_in_pt


def get_formula_by_id(*, session: Session, formula_id: int) -> Formula:
    return session.get(Formula, formula_id)


def get_formula_by_formula_str(*, session: Session, formula_str: str) -> Formula | None:
    statement = select(Formula).where(Formula.formula_string == formula_str)
    db_formula = session.exec(statement).first()
    if db_formula:
        return db_formula
    else:
        return None


def get_formulas_by_conditions(
    *,
    session: Session,
    formula_filter: FormulaFilter = None,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[Formula]:
    query = select(Formula)
    if formula_filter:
        for numeric_filter in formula_filter.numeric_filters:
            if numeric_filter.column in ("molwt", "atom_number"):
                query = query.where(
                    getattr(Formula, numeric_filter.column) >= numeric_filter.min
                ).where(getattr(Formula, numeric_filter.column) <= numeric_filter.max)
        for element_filter in formula_filter.element_filters:
            if element_filter.element not in elements_in_pt:
                continue
            if element_filter.count < 0:
                query = query.where(getattr(Formula, element_filter.element) > 0)
            else:
                query = query.where(
                    getattr(Formula, element_filter.element) == element_filter.count
                )
    statement = query.offset(skip).limit(limit)
    db_formulas = session.exec(statement).all()
    return db_formulas

def get_formula_count(*, session: Session) -> ItemCount:
    count_statement = select(func.count()).select_from(Formula)
    count = session.exec(count_statement).one()
    return ItemCount(count=count)

