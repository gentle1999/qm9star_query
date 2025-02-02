import os
from typing import Any, List, Literal

from qm9star_query.api.deps import SessionDep
from qm9star_query.crud import formulas_crud
from qm9star_query.models import Formula
from qm9star_query.models.formula import FormulaOut, FormulasOut
from qm9star_query.models.utils import ItemCount, FormulaFilter
from fastapi import APIRouter, HTTPException
from sqlmodel import column, func, select

router = APIRouter()


@router.get("/{id}", response_model=FormulaOut)
def read_formula_by_id(session: SessionDep, id: int) -> Any:
    """
    Get a formula by id
    """
    formula = formulas_crud.get_formula_by_id(session=session, formula_id=id)
    if not formula:
        raise HTTPException(status_code=404, detail="Formula not found")
    return FormulaOut.model_validate(formula)


@router.get("/count/", response_model=ItemCount)
def read_formulas_count(
    session: SessionDep,
) -> ItemCount:
    """
    Get the number of formulas in the database.
    """
    count_statement = select(func.count()).select_from(Formula)
    count = session.exec(count_statement).one()
    return ItemCount(count=count)


@router.get("/", response_model=FormulasOut)
def read_formulas(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve formulas.
    """
    statement = select(Formula).offset(skip).limit(limit)
    formulas = session.exec(statement).all()

    return FormulasOut(data=formulas, count=len(formulas))


@router.post("/filter/", response_model=FormulasOut)
def read_formulas_by_filter(
    session: SessionDep,
    filters: FormulaFilter = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve formulas by filter. 

    Detailed filters setting can be found in the schema of `FormulaFilter`.
    """
    formulas = formulas_crud.get_formulas_by_conditions(
        session=session,
        formula_filter=filters,
        skip=skip,
        limit=limit,
    )
    return FormulasOut(data=formulas, count=len(formulas))


