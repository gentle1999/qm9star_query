import os
from typing import Literal

from fastapi import APIRouter, HTTPException
from rdkit import Chem
from sqlmodel import col, column, func, select

from qm9star_query.api.deps import SessionDep
from qm9star_query.crud import molecules_crud, snapshots_crud
from qm9star_query.models import Molecule, Snapshot
from qm9star_query.models.snapshot import SnapshotOut, SnapshotSDFOut, SnapshotsOut
from qm9star_query.models.utils import ItemCount,  SnapshotFilter
from qm9star_query.utils import recover_rdmol_from_snapshot

router = APIRouter()


@router.get("/{id}", response_model=SnapshotOut)
def read_snapshot_by_id(session: SessionDep, id: int) -> SnapshotOut:
    """
    Get a snapshot by id.
    """
    snapshot = session.get(Snapshot, id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return SnapshotOut.model_validate(snapshot)


@router.get("/sdf/{id}", response_model=SnapshotSDFOut)
def read_snapshot_sdf_by_id(session: SessionDep, id: int) -> SnapshotSDFOut:
    """
    Get a snapshot by id.
    """
    snapshot = session.get(Snapshot, id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    rdmol = recover_rdmol_from_snapshot(snapshot)
    return SnapshotSDFOut(
        smiles=snapshot.molecule.smiles,
        sdf_block=Chem.MolToMolBlock(rdmol),
    )


@router.get("/count/", response_model=ItemCount)
def read_snapshots_count(
    session: SessionDep,
) -> ItemCount:
    """
    Get the number of snapshots in the database.
    """
    count_statement = select(func.count()).select_from(Snapshot)
    count = session.exec(count_statement).one()
    return ItemCount(count=count)


@router.get("/", response_model=SnapshotsOut)
def read_snapshots(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> SnapshotsOut:
    """
    Retrieve snapshots.
    """
    statement = select(Snapshot).offset(skip).limit(limit)
    snapshots = session.exec(statement).all()

    return SnapshotsOut(snapshots=snapshots, count=len(snapshots))


@router.get("/smiles/", response_model=SnapshotsOut)
def read_snapshots_by_smiles(
    session: SessionDep,
    smiles: str,
    method: Literal["morgan", "rdk", "atompair", "torsion"] = "morgan",
    distance: Literal["l2", "inner_product", "cosine"] = "l2",
    skip: int = 0,
    limit: int = 1,
) -> SnapshotsOut:
    """
    Fuzzy search through SMILES

    The SMILES string will be transformed into an embedding you selected and used to find
    similar molecules in the database by vector distance.

    In detail, this function will search the Molecules similar to the SMILES passed (skip
    and limit work here.). Then offer the snapshots belonging to the molecules. Therefore,
    the number of snapshots returned may greater than the limit.

    We recommend using `limit=1`, which will return all snapshots of the molecule that
    most closely match a given SMILES.
    """
    db_snapshots = snapshots_crud.get_snapshots_by_conditions(
        session=session,
        snapshot_filter=SnapshotFilter(
            smiles=smiles,
            method=method,
            distance=distance,
            numeric_filters=[],
            class_filters=[],
            bool_filters=[],
            element_filters=[],
        ),
        skip=skip,
        limit=limit,
    )
    return SnapshotsOut(snapshots=db_snapshots, count=len(db_snapshots))


@router.get("/smiles_strict/", response_model=SnapshotsOut)
def read_snapshots_by_smiles_strict_match(
    session: SessionDep, smiles: str
) -> SnapshotsOut:
    """
    Precise search through SMILES
    """
    db_molecule = molecules_crud.get_molecule_by_smiles(session=session, smiles=smiles)
    if db_molecule:
        return SnapshotsOut(
            snapshots=db_molecule.snapshots, count=len(db_molecule.snapshots)
        )
    else:
        raise HTTPException(status_code=404, detail="Molecule not found")


@router.post("/filter/", response_model=SnapshotsOut)
def read_molecules_by_filter(
    session: SessionDep,
    filters: SnapshotFilter = None,
    skip: int = 0,
    limit: int = 5,
) -> SnapshotsOut:
    """
    Retrieve snapshots by filters.

    Detailed filters setting can be found in the schema of `SnapshotFilter`.
    """
    db_snapshots = snapshots_crud.get_snapshots_by_conditions(
        session=session,
        snapshot_filter=filters,
        skip=skip,
        limit=limit,
    )
    return SnapshotsOut(snapshots=db_snapshots, count=len(db_snapshots))
