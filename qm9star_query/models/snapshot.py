from datetime import datetime
from typing import List

from sqlalchemy import ARRAY, Column, Float, Integer
from sqlmodel import Field, SQLModel


class SnapshotBase(SQLModel):
    # Molecule graph information, fully recoverable
    filename: str = Field(default=None)
    frame_id: int = Field(default=None)
    coords: List[List[float]] = Field(sa_column=Column(ARRAY(Float, dimensions=2)))
    atoms: List[int] = Field(sa_column=Column(ARRAY(Integer)))
    bonds: List[List[int]] = Field(sa_column=Column(ARRAY(Integer, dimensions=2)))
    formal_charges: List[int] = Field(sa_column=Column(ARRAY(Integer)))
    formal_spins: List[int] = Field(sa_column=Column(ARRAY(Integer)))
    standard_coords: List[List[float]] = Field(sa_column=Column(ARRAY(Float, dimensions=2)))

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
    temperature: float = Field(default=298.15)

    # QM properties
    mulliken_charge: List[float] | None = Field(
        sa_column=Column(ARRAY(Float)), default=[]
    )
    spin_densities: List[float] | None = Field(
        sa_column=Column(ARRAY(Float)), default=[]
    )
    gradients: List[List[float]] | None = Field(
        sa_column=Column(ARRAY(Float, dimensions=2)), default=[[]]
    )
    single_point_energy: float | None = Field(default=None, nullable=True)
    zero_point_correction: float | None = Field(default=None, nullable=True)
    energy_correction: float | None = Field(default=None, nullable=True)
    enthalpy_correction: float | None = Field(default=None, nullable=True)
    gibbs_free_energy_correction: float | None = Field(default=None, nullable=True)
    zero_point_sum: float | None = Field(default=None, nullable=True)
    thermal_energy_sum: float | None = Field(default=None, nullable=True)
    thermal_enthalpy_sum: float | None = Field(default=None, nullable=True)
    thermal_free_energy_sum: float | None = Field(default=None, nullable=True)

    alpha_homo: float | None = Field(default=None, nullable=True)
    alpha_lumo: float | None = Field(default=None, nullable=True)
    alpha_gap: float | None = Field(default=None, nullable=True)
    beta_homo: float | None = Field(default=None, nullable=True)
    beta_lumo: float | None = Field(default=None, nullable=True)
    beta_gap: float | None = Field(default=None, nullable=True)
    first_frequency: float | None = Field(default=None, nullable=True)
    first_vibration_mode: List[float] | None = Field(
        sa_column=Column(ARRAY(Float)), default=[]
    )
    second_frequency: float | None = Field(default=None, nullable=True)
    second_vibration_mode: List[float] | None = Field(
        sa_column=Column(ARRAY(Float)), default=[]
    )
    spin_eginvalue: float | None = Field(default=None, nullable=True)
    spin_multiplicity: float | None = Field(default=None, nullable=True)
    dipole: List[float] | None = Field(sa_column=Column(ARRAY(Float)), default=[])
    quadrupole: List[float] | None = Field(sa_column=Column(ARRAY(Float)), default=[])
    octapole: List[float] | None = Field(sa_column=Column(ARRAY(Float)), default=[])
    hexadecapole: List[float] | None = Field(
        sa_column=Column(ARRAY(Float)), default=[]
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
    nbo_charges: List[float] | None = Field(
        sa_column=Column(ARRAY(Float)), default=[]
    )
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


class SnapshotCreate(SnapshotBase):...


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
    formal_spins: List[int] | None = Field(
        sa_column=Column(ARRAY(Integer)), default=None
    )

    owner_id: int | None = None
    update_time: datetime = Field(default_factory=datetime.now)


class SnapshotSDFOut(SQLModel):
    smiles: str
    sdf_block: str