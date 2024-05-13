from datetime import datetime
from typing import List

from sqlalchemy import ARRAY, Column, Float, Integer
from sqlmodel import Field, SQLModel

from qm9star_query.models.molecule import MoleculeOut


class SnapshotBase(SQLModel):
    # Molecule graph information, fully recoverable
    filename: str = Field(default=None)
    frame_id: int = Field(default=None)
    coords: List[List[float]] = Field(
        sa_column=Column(ARRAY(Float, dimensions=2), comment="Unit: Angstrom"),
        description="Unit: Angstrom",
    )
    atoms: List[int] = Field(sa_column=Column(ARRAY(Integer)))
    bonds: List[List[int]] = Field(sa_column=Column(ARRAY(Integer, dimensions=2)))
    formal_charges: List[int] = Field(sa_column=Column(ARRAY(Integer)))
    formal_num_radicals: List[int] = Field(sa_column=Column(ARRAY(Integer)))
    standard_coords: List[List[float]] = Field(
        sa_column=Column(ARRAY(Float, dimensions=2), comment="Unit: Angstrom"),
        description="Unit: Angstrom",
    )

    # qm software basic information
    qm_software: str | None = Field(default=None, nullable=True)
    qm_software_version: str | None = Field(default=None, nullable=True)
    basis: str | None = Field(default=None, nullable=True)
    functional: str | None = Field(default=None, nullable=True)
    keywords: str | None = Field(default=None, nullable=True)

    # Solvent
    solvent_model: str | None = Field(default=None, nullable=True)
    solvent: str | None = Field(default=None, nullable=True)

    # Thermodynamic setting
    temperature: float = Field(
        default=298.15,
        description="Unit: Kelvin",
        sa_column_kwargs={"comment": "Unit: Kelvin"},
    )

    # QM properties
    mulliken_charge: List[float] | None = Field(
        sa_column=Column(ARRAY(Float)), default=[]
    )
    spin_densities: List[float] | None = Field(
        sa_column=Column(ARRAY(Float)), default=[]
    )
    gradients: List[List[float]] | None = Field(
        sa_column=Column(ARRAY(Float, dimensions=2), comment="Unit: hartree/bohr"),
        default=[[]],
        description="Unit: hartree/bohr",
    )
    single_point_energy: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: hartree/particle",
        sa_column_kwargs={"comment": "Unit: hartree/particle"},
    )
    zpve: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: hartree/particle",
        sa_column_kwargs={"comment": "Unit: hartree/particle"},
    )
    energy_correction: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: hartree/particle",
        sa_column_kwargs={"comment": "Unit: hartree/particle"},
    )
    enthalpy_correction: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: hartree/particle",
        sa_column_kwargs={"comment": "Unit: hartree/particle"},
    )
    gibbs_free_energy_correction: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: hartree/particle",
        sa_column_kwargs={"comment": "Unit: hartree/particle"},
    )
    U_0: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: hartree/particle",
        sa_column_kwargs={"comment": "Unit: hartree/particle"},
    )
    U_T: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: hartree/particle",
        sa_column_kwargs={"comment": "Unit: hartree/particle"},
    )
    H_T: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: hartree/particle",
        sa_column_kwargs={"comment": "Unit: hartree/particle"},
    )
    G_T: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: hartree/particle",
        sa_column_kwargs={"comment": "Unit: hartree/particle"},
    )
    S: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: cal/mol/K",
        sa_column_kwargs={"comment": "Unit: cal/mol/K"},
    )
    Cv: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: cal/mol/K",
        sa_column_kwargs={"comment": "Unit: cal/mol/K"},
    )
    rotation_consts: List[float] | None = Field(
        sa_column=Column(ARRAY(Float), comment="Unit: Ghz"),
        default=[],
        description="Unit: Ghz",
    )
    isotropic_polarizability: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: bohr^3",
        sa_column_kwargs={"comment": "Unit: bohr^3"},
    )
    electronic_spatial_extent: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: bohr^2",
        sa_column_kwargs={"comment": "Unit: bohr^2"},
    )
    alpha_homo: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: hartree/particle",
        sa_column_kwargs={"comment": "Unit: hartree/particle"},
    )
    alpha_lumo: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: hartree/particle",
        sa_column_kwargs={"comment": "Unit: hartree/particle"},
    )
    alpha_gap: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: hartree/particle",
        sa_column_kwargs={"comment": "Unit: hartree/particle"},
    )
    beta_homo: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: hartree/particle",
        sa_column_kwargs={"comment": "Unit: hartree/particle"},
    )
    beta_lumo: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: hartree/particle",
        sa_column_kwargs={"comment": "Unit: hartree/particle"},
    )
    beta_gap: float | None = Field(
        default=None,
        nullable=True,
        description="Unit: hartree/particle",
        sa_column_kwargs={"comment": "Unit: hartree/particle"},
    )
    freqs: List[float] | None = Field(
        sa_column=Column(ARRAY(Float), comment="Unit: cm^-1"),
        default=[],
        description="Unit: cm^-1",
    )
    reduced_masses: List[float] | None = Field(
        sa_column=Column(ARRAY(Float), comment="Unit: amu"),
        default=[],
        description="Unit: amu",
    )
    IR_intensities: List[float] | None = Field(
        sa_column=Column(ARRAY(Float), comment="Unit: kmol/mol"),
        default=[],
        description="Unit: kmol/mol",
    )
    force_constants: List[float] | None = Field(
        sa_column=Column(ARRAY(Float), comment="Unit: mdyne/angstrom"),
        default=[],
        description="Unit: mdyne/angstrom",
    )
    spin_quantum_number: float | None = Field(default=None, nullable=True)
    spin_square: float | None = Field(default=None, nullable=True)
    dipole: List[float] | None = Field(
        sa_column=Column(ARRAY(Float), comment="Unit: debye"),
        default=[],
        description="Unit: debye",
    )
    quadrupole: List[float] | None = Field(
        sa_column=Column(ARRAY(Float), comment="Unit: debye-angstrom"),
        default=[],
        description="Unit: debye-angstrom",
    )
    octapole: List[float] | None = Field(
        sa_column=Column(ARRAY(Float), comment="Unit: debye-angstrom^2"),
        default=[],
        description="Unit: debye-angstrom^2",
    )
    hexadecapole: List[float] | None = Field(
        sa_column=Column(ARRAY(Float), comment="Unit: debye-angstrom^3"),
        default=[],
        description="Unit: debye-angstrom^3",
    )
    nbo_bond_order: List[List[float]] | None = Field(
        sa_column=Column(ARRAY(Float, dimensions=2)), default=[[]]
    )
    wiberg_bond_order: List[List[float]] | None = Field(
        sa_column=Column(ARRAY(Float, dimensions=2)), default=[[]]
    )
    mo_bond_order: List[List[float]] | None = Field(
        sa_column=Column(ARRAY(Float, dimensions=2)), default=[[]]
    )
    atom_atom_overlap_bond_order: List[List[float]] | None = Field(
        sa_column=Column(ARRAY(Float, dimensions=2)), default=[[]]
    )
    nbo_charges: List[float] | None = Field(sa_column=Column(ARRAY(Float)), default=[])
    lowdin_charges: List[float] | None = Field(
        sa_column=Column(ARRAY(Float)), default=[]
    )
    hirshfeld_charges: List[float] | None = Field(
        sa_column=Column(ARRAY(Float)), default=[]
    )

    # status properties
    is_TS: bool = Field(default=False)
    is_optimized: bool = Field(default=False)
    is_error: bool = Field(default=False)


class SnapshotCreate(SnapshotBase): ...


class SnapshotUpdate(SnapshotBase):
    # Molecule graph information, fully recoverable
    coords: List[List[float]] | None = Field(
        sa_column=Column(ARRAY(Float, dimensions=2)), default=None
    )
    atoms: List[int] | None = Field(sa_column=Column(ARRAY(Integer)), default=None)
    bonds: List[List[int]] | None = Field(
        sa_column=Column(ARRAY(Integer, dimensions=2), default=None)
    )
    formal_charges: List[int] | None = Field(
        sa_column=Column(ARRAY(Integer)), default=None
    )
    formal_num_radicals: List[int] | None = Field(
        sa_column=Column(ARRAY(Integer)), default=None
    )

    owner_id: int | None = None
    update_time: datetime = Field(default_factory=datetime.now)


class SnapshotOut(SnapshotBase):
    id: int
    commit_time: datetime
    update_time: datetime

    molecule: MoleculeOut


class SnapshotSDFOut(SQLModel):
    smiles: str
    sdf_block: str
