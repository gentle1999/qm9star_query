from datetime import datetime
from typing import List

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlmodel import Field, SQLModel

from qm9star_query.models.formula import FormulaOut


class MoleculeBase(SQLModel):
    # Topological properties of the molecule
    smiles: str = Field(index=True, unique=True)
    inchi: str = Field(index=True)
    canonical_smiles: str = Field(index=True)
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


class MoleculeOut(SQLModel):
    id: int
    smiles: str = Field(description="The SMILES string of the molecule")
    inchi: str = Field(description="The InChI string of the molecule")
    canonical_smiles: str = Field(
        description="The canonical SMILES string of the molecule"
    )
    total_charge: int = Field(description="The total charge of the molecule")
    total_multiplicity: int = Field(
        description="The total multiplicity of the molecule"
    )
    qed: float | None = Field(
        description="The Quantitative Estimation of Drug-likeness (QED) of the molecule",
        default=None,
    )
    logp: float | None = Field(description="The LogP of the molecule", default=None)

    formula: FormulaOut | None = Field(
        description="The `Formula` of the molecule", default=None
    )

    commit_time: datetime = Field(
        description="The time when the data is committed to the database"
    )
    update_time: datetime = Field(description="The time when the data is last updated")


class MoleculeSDFOut(SQLModel):
    smiles: str = Field(description="The SMILES string of the molecule")
    sdf_block: str = Field(description="The 2D SDF block of the molecule")


class MoleculesOut(SQLModel):
    count: int = Field(description="The count of molecules in the query result")
    data: list[MoleculeOut] = Field(
        description="The list of `Molecule` objects in the query result"
    )
