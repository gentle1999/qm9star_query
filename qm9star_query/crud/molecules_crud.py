from typing import Literal, Sequence

from qm9star_query.models import Formula, Molecule
from qm9star_query.models.utils import MoleculeFilter, ItemCount
from qm9star_query.utils import (
    elements_in_pt,
    smi_to_embedding,
    smiles_to_formula_dict,
)
from sqlmodel import Session, select, func


def get_molecule_by_id(*, session: Session, molecule_id: int) -> Molecule:
    return session.get(Molecule, molecule_id)


def get_molecule_by_smiles(*, session: Session, smiles: str) -> Molecule:
    formula_dict = smiles_to_formula_dict(smiles)
    formula_str = "".join(
        [f"{symbol}{element}" for symbol, element in formula_dict.items()]
    )
    session_molecule = session.exec(
        select(Molecule)
        .join(Formula)
        .where(Formula.formula_string == formula_str)
        .where(Molecule.smiles == smiles)
    ).first()
    return session_molecule


def get_molecules_by_smiles(
    *,
    session: Session,
    smiles: str,
    method: Literal["morgan", "rdk", "atompair", "torsion"] = "morgan",
    distance: Literal["l2", "inner_product", "cosine"] = "cosine",
    skip: int = 0,
    limit: int = 5,
) -> Sequence[Molecule]:
    embedding = smi_to_embedding(smiles, method)
    query = select(Molecule)
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
    session_molecules = session.exec(query.offset(skip).limit(limit)).all()
    return session_molecules


def get_molecules_by_conditions(
    *,
    session: Session,
    molecule_filter: MoleculeFilter = None,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[Molecule]:
    query = select(Molecule).join(Formula)
    if molecule_filter:
        for element_filter in molecule_filter.element_filters:
            if element_filter.element not in elements_in_pt:
                continue
            if element_filter.count < 0:
                query = query.where(getattr(Formula, element_filter.element) > 0)
            else:
                query = query.where(
                    getattr(Formula, element_filter.element) == element_filter.count
                )
        for numeric_filter in molecule_filter.numeric_filters:
            if numeric_filter.column in ("molwt", "atom_number"):
                query = query.where(
                    getattr(Formula, numeric_filter.column) >= numeric_filter.min
                ).where(getattr(Formula, numeric_filter.column) <= numeric_filter.max)
            if numeric_filter.column in (
                "atom_number",
                "total_multiplicity",
                "qed",
                "logp",
            ):
                query = query.where(
                    getattr(Molecule, numeric_filter.column) >= numeric_filter.min
                ).where(getattr(Molecule, numeric_filter.column) <= numeric_filter.max)
        if molecule_filter.smiles:
            embedding = smi_to_embedding(molecule_filter.smiles, molecule_filter.method)
            method = molecule_filter.method
            distance = molecule_filter.distance
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
    db_molecules = session.exec(statement).all()
    return db_molecules

def get_molecule_count(*, session: Session) -> ItemCount:
    count_statement = select(func.count()).select_from(Molecule)
    count = session.exec(count_statement).one()
    return ItemCount(count=count)
