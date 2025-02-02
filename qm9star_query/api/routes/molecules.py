import os
from typing import Any, List, Literal

from fastapi import APIRouter, HTTPException
from rdkit import Chem
from sqlmodel import column, func, select

from qm9star_query.api.deps import SessionDep
from qm9star_query.crud import molecules_crud
from qm9star_query.models import Formula, Molecule
from qm9star_query.models.molecule import MoleculeOut, MoleculeSDFOut, MoleculesOut
from qm9star_query.models.utils import ItemCount, MoleculeFilter

router = APIRouter()


@router.get("/{id}", response_model=MoleculeOut)
def read_molecule_by_id(session: SessionDep, id: int):
    """
    Get molecule by id
    """
    molecule = session.get(Molecule, id)
    if not molecule:
        raise HTTPException(status_code=404, detail="Molecule not found")
    return MoleculeOut.model_validate(molecule)


@router.get("/sdf/{id}", response_model=MoleculeSDFOut)
def read_molecule_sdf_by_id(session: SessionDep, id: int):
    """
    Get sdf of molecule by id
    """
    molecule = session.get(Molecule, id)
    if not molecule:
        raise HTTPException(status_code=404, detail="Molecule not found")
    return MoleculeSDFOut(
        smiles=molecule.smiles,
        sdf_block=Chem.MolToMolBlock(Chem.MolFromSmiles(molecule.smiles)),
    )


@router.get("/count/", response_model=ItemCount)
def read_molecules_count(
    session: SessionDep,
) -> ItemCount:
    """
    Get the number of molecules in the database.
    """
    count_statement = select(func.count()).select_from(Molecule)
    count = session.exec(count_statement).one()
    return ItemCount(count=count)


@router.get("/", response_model=MoleculesOut)
def read_molecules(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve molecules.
    """
    statement = select(Molecule).offset(skip).limit(limit)
    molecules = session.exec(statement).all()

    return MoleculesOut(data=molecules, count=len(molecules))


@router.get("/smiles/", response_model=MoleculesOut)
def read_molecules_by_smiles(
    session: SessionDep,
    smiles: str,
    skip: int = 0,
    limit: int = 5,
    method: Literal["morgan", "rdk", "atompair", "torsion"] = "morgan",
    distance: Literal["l2", "inner_product", "cosine"] = "cosine",
) -> MoleculesOut:
    """
    Fuzzy search through SMILES

    The SMILES string will be transformed into an embedding you selected and used to find
    similar molecules in the database by vector distance.

    SLOW: This method is very slow for large datasets.
    """
    db_molecules = molecules_crud.get_molecules_by_smiles(
        session=session,
        smiles=smiles,
        method=method,
        distance=distance,
        skip=skip,
        limit=limit,
    )
    return MoleculesOut(data=db_molecules, count=len(db_molecules))


@router.get("/smiles_strict/", response_model=MoleculeOut)
def read_molecule_by_smiles_strict_match(
    session: SessionDep,
    smiles: str,
) -> MoleculeOut:
    """
    Precise search through SMILES
    """
    db_molecule = molecules_crud.get_molecule_by_smiles(
        session=session, smiles=smiles
    )
    if not db_molecule:
        raise HTTPException(status_code=404, detail="Molecule not found")
    return MoleculeOut.model_validate(db_molecule)


@router.post("/filter/", response_model=MoleculesOut)
def read_molecules_by_filter(
    session: SessionDep,
    filters: MoleculeFilter = None,
    skip: int = 0,
    limit: int = 100,
) -> MoleculesOut:
    """
    Retrieve molecules by filters.

    Detailed filters setting can be found in the schema of `MoleculeFilter`.
    """
    session_molecules = molecules_crud.get_molecules_by_conditions(
        session=session,
        molecule_filter=filters,
        skip=skip,
        limit=limit,
    )
    return MoleculesOut(data=session_molecules, count=len(session_molecules))
