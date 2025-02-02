from datetime import datetime
from typing import List, Literal

from sqlmodel import Field, SQLModel


class NumericFilter(SQLModel):
    """
    ## Available columns for `FormulaFilter`:
    - "molwt"
    - "atom_number"
    ## Available columns for `MoleculeFilter`:
    except above columns, there are also:
    - "total_multiplicity"
    - "total_charge"
    - "qed"
    - "logp"
    ## Available columns for `SnapshotFilter`:
    except above columns, there are also:
    - "temperature"
    - "single_point_energy"
    - "zpve"
    - "energy_correction"
    - "enthalpy_correction"
    - "gibbs_free_energy_correction"
    - "U_0"
    - "U_T"
    - "H_T"
    - "G_T"
    - "S"
    - "Cv"
    - "isotropic_polarizability"
    - "electronic_spatial_extent"
    - "alpha_homo"
    - "alpha_lumo"
    - "alpha_gap"
    - "beta_homo"
    - "beta_lumo"
    - "beta_gap"
    - "first_frequency"
    - "second_frequency"
    - "spin_quantum_number"
    - "spin_square"
    """

    column: str = Field(description="column name", default="atom_number")
    min: float = Field(
        description="minimum value, default is negative infinity", default=float("-inf")
    )
    max: float = Field(
        description="maximum value, default is positive infinity", default=float("inf")
    )


class ElementFilter(SQLModel):
    element: str = Field(description="element symbol like 'C', 'He', 'Os'", default="C")
    count: int = Field(
        default=1, description="-1 for existing, 0 for non-existing, >0 for count"
    )


class FormulaFilter(SQLModel):
    numeric_filters: List[NumericFilter] = Field(
        description="list of `NumericFilter`, default is empty", default_factory=list
    )
    element_filters: List[ElementFilter] = Field(
        description="list of `ElementFilter`, default is empty", default_factory=list
    )


class MoleculeFilter(SQLModel):
    smiles: str | None = Field(
        description="SMILES string, excute slow vector search if not None", default=None
    )
    method: Literal["morgan", "rdk", "atompair", "torsion"] = Field(
        description="fingerprint method", default="morgan"
    )
    distance: Literal["l2", "inner_product", "cosine"] = Field(
        description="distance metric", default="cosine"
    )
    numeric_filters: List[NumericFilter] = Field(
        description="list of `NumericFilter`, default is empty", default_factory=list
    )
    element_filters: List[ElementFilter] = Field(
        description="list of `ElementFilter`, default is empty", default_factory=list
    )


class ClassFilter(SQLModel):
    column: Literal[
        "filename",
        "qm_software",
        "qm_software_version",
        "basis",
        "functional",
        "keywords",
        "solvent_model",
        "solvent",
    ] = Field(description="column name", default="filename")
    values: List[str | int] = Field(
        description="list of values, if entry matches any value, it will be included",
        default_factory=list,
    )


class BoolFilter(SQLModel):
    column: Literal["is_TS", "is_optimized", "is_error"] = Field(
        description="column name"
    )
    value: bool = Field(description="True or False", default=True)


class SnapshotFilter(SQLModel):
    numeric_filters: List[NumericFilter] = Field(
        description="list of `NumericFilter`, default is empty", default_factory=list
    )
    class_filters: List[ClassFilter] = Field(
        description="list of `ClassFilter`, default is empty", default_factory=list
    )
    bool_filters: List[BoolFilter] = Field(
        description="list of `BoolFilter`, default is empty", default_factory=list
    )
    element_filters: List[ElementFilter] = Field(
        description="list of `ElementFilter`, default is empty", default_factory=list
    )
    smiles: str | None = Field(
        description="SMILES string, excute slow vector search if not None", default=None
    )
    method: Literal["morgan", "rdk", "atompair", "torsion"] = Field(
        description="fingerprint method", default="morgan"
    )
    distance: Literal["l2", "inner_product", "cosine"] = Field(
        description="distance metric", default="cosine"
    )


class ItemCount(SQLModel):
    count: int = Field(description="number of items")
