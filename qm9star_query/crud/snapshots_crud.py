from typing import Sequence

from qm9star_query.models import Formula, Molecule, Snapshot
from qm9star_query.models.utils import SnapshotFilter, ItemCount
from qm9star_query.utils import (
    elements_in_pt,
    smi_to_embedding,
    smiles_to_formula_dict,
)
from sqlmodel import Session, col, select, func
def get_snapshot_by_id(*, session: Session, snapshot_id: int) -> Snapshot:
    return session.get(Snapshot, snapshot_id)


def get_snapshot_by_smiles_hash(*, session: Session, smiles: str, snapshot_hash: str):
    formula_dict = smiles_to_formula_dict(smiles)
    formula_str = "".join(
        [f"{symbol}{element}" for symbol, element in formula_dict.items()]
    )
    db_snapshot = session.exec(
        select(Snapshot)
        .join(Molecule)
        .join(Formula)
        .where(Formula.formula_string == formula_str)
        .where(Molecule.smiles == smiles)
        .where(Snapshot.hash_token == snapshot_hash)
    ).first()
    return db_snapshot


def get_snapshots_by_conditions(
    *,
    session: Session,
    snapshot_filter: SnapshotFilter = None,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[Snapshot]:
    query = select(Snapshot).join(Molecule).join(Formula)
    if snapshot_filter:
        for element_filter in snapshot_filter.element_filters:
            if element_filter.element not in elements_in_pt:
                continue
            if element_filter.count < 0:
                query = query.where(getattr(Formula, element_filter.element) > 0)
            else:
                query = query.where(
                    getattr(Formula, element_filter.element) == element_filter.count
                )
        for numeric_filter in snapshot_filter.numeric_filters:
            if numeric_filter.column in ("atom_number", "molwt"):
                query = query.where(
                    getattr(Formula, numeric_filter.column) >= numeric_filter.min
                ).where(getattr(Formula, numeric_filter.column) <= numeric_filter.max)
            elif numeric_filter.column in (
                "atom_number",
                "total_multiplicity",
                "qed",
                "logp",
            ):
                query = query.where(
                    getattr(Molecule, numeric_filter.column) >= numeric_filter.min
                ).where(getattr(Molecule, numeric_filter.column) <= numeric_filter.max)
            elif numeric_filter.column in (
                "single_point_energy",
                "zero_point_correction",
                "energy_correction",
                "enthalpy_correction",
                "gibbs_free_energy_correction",
                "zero_point_sum",
                "thermal_energy_sum",
                "thermal_enthalpy_sum",
                "thermal_free_energy_sum",
                "alpha_homo",
                "alpha_lumo",
                "alpha_gap",
                "beta_homo",
                "beta_lumo",
                "beta_gap",
                "spin_eginvalue",
                "spin_multiplicity",
            ):
                query = query.where(
                    getattr(Snapshot, numeric_filter.column) >= numeric_filter.min
                ).where(getattr(Snapshot, numeric_filter.column) <= numeric_filter.max)
        for class_filter in snapshot_filter.class_filters:
            if hasattr(Snapshot, class_filter.column):
                query = query.where(
                    col(getattr(Snapshot, class_filter.column)).in_(class_filter.values)
                )
        for bool_filter in snapshot_filter.bool_filters:
            if hasattr(Snapshot, bool_filter.column):
                query = query.where(
                    getattr(Snapshot, bool_filter.column) == bool_filter.value
                )
        if snapshot_filter.smiles:
            embedding = smi_to_embedding(snapshot_filter.smiles, snapshot_filter.method)
            method = snapshot_filter.method
            distance = snapshot_filter.distance
            if method == "morgan":
                fp = Molecule.morgan_fp3_1024
            elif method == "rdk":
                fp = Molecule.rdkit_fp_1024
            elif method == "atompair":
                fp = Molecule.atompair_fp_1024
            elif method == "torsion":
                fp = Molecule.topological_torsion_fp_1024
            else:
                raise ValueError("Invalid embedding method")
            if distance == "l2":
                query = query.order_by(fp.l2_distance(embedding))
            elif distance == "inner_product":
                query = query.order_by(fp.max_inner_product(embedding))
            elif distance == "cosine":
                query = query.order_by(fp.cosine_distance(embedding))
    statement = query.offset(skip).limit(limit)
    return session.exec(statement).all()

def get_snapshot_count(*, session: Session) -> ItemCount:
    count_statement = select(func.count()).select_from(Snapshot)
    count = session.exec(count_statement).one()
    return ItemCount(count=count)