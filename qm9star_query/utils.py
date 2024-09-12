import hashlib
from typing import List, Literal

from rdkit import Chem
from rdkit.Chem import AllChem

from qm9star_query.models import Snapshot

pt = Chem.GetPeriodicTable()
elements_in_pt = [pt.GetElementSymbol(i) for i in range(1, 119)]
bond_list = [
    Chem.rdchem.BondType.UNSPECIFIED,
    Chem.rdchem.BondType.SINGLE,
    Chem.rdchem.BondType.DOUBLE,
    Chem.rdchem.BondType.TRIPLE,
    Chem.rdchem.BondType.QUADRUPLE,
    Chem.rdchem.BondType.QUINTUPLE,
    Chem.rdchem.BondType.HEXTUPLE,
    Chem.rdchem.BondType.ONEANDAHALF,
    Chem.rdchem.BondType.TWOANDAHALF,
    Chem.rdchem.BondType.THREEANDAHALF,
    Chem.rdchem.BondType.FOURANDAHALF,
    Chem.rdchem.BondType.FIVEANDAHALF,
    Chem.rdchem.BondType.AROMATIC,
    Chem.rdchem.BondType.IONIC,
    Chem.rdchem.BondType.HYDROGEN,
    Chem.rdchem.BondType.THREECENTER,
    Chem.rdchem.BondType.DATIVEONE,
    Chem.rdchem.BondType.DATIVE,
    Chem.rdchem.BondType.DATIVEL,
    Chem.rdchem.BondType.DATIVER,
    Chem.rdchem.BondType.OTHER,
    Chem.rdchem.BondType.ZERO,
]


class rdkit_fpgen:
    morgan_fpgen = AllChem.GetMorganGenerator(
        radius=3, fpSize=1024, includeChirality=True
    )
    atompair_fpgen = AllChem.GetAtomPairGenerator(fpSize=1024, includeChirality=True)
    rdkit_fpgen = AllChem.GetRDKitFPGenerator(fpSize=1024)
    topological_torsion_fpgen = AllChem.GetTopologicalTorsionGenerator(fpSize=1024)


def smi_to_embedding(
    smiles: str, method: Literal["morgan", "rdk", "atompair", "torsion"]
) -> List[int]:
    try:
        rdmol = Chem.AddHs(Chem.MolFromSmiles(smiles))
    except:
        raise ValueError("Invalid SMILES")
    if method == "morgan":
        return rdkit_fpgen.morgan_fpgen.GetFingerprint(rdmol).ToList()
    elif method == "rdk":
        return rdkit_fpgen.rdkit_fpgen.GetFingerprint(rdmol).ToList()
    elif method == "atompair":
        return rdkit_fpgen.atompair_fpgen.GetFingerprint(rdmol).ToList()
    elif method == "torsion":
        return rdkit_fpgen.topological_torsion_fpgen.GetFingerprint(rdmol).ToList()
    else:
        raise ValueError("Invalid method")


def check_smi_equal(smi1: str, smi2: str):
    if smi1 == smi2:
        return True
    if Chem.CanonSmiles(smi1) == Chem.CanonSmiles(smi2):
        return True
    mol1 = Chem.MolFromSmiles(smi1)
    mol2 = Chem.MolFromSmiles(smi2)
    if mol1.GetSubstructMatch(mol2) and mol2.GetSubstructMatch(mol1):
        return True
    return False


def get_snapshot_hash_token(snapshot: Snapshot):
    pattern = snapshot.model_dump_json(
        include={
            "coords",
            "atoms",
            "bonds",
            "formal_charges",
            "formal_num_radicals",
            "qm_software",
            "qm_software_version",
            "basis",
            "functional",
            "keywords",
            "solvent_model",
            "solvent",
            "temperature",
        }
    )
    return hashlib.sha256(pattern.encode("utf-8")).hexdigest()


def recover_rdmol(
    coords: List[List[float]],
    atoms: List[str],
    bonds: List[List[int]],
    formal_charges: List[int],
    formal_num_radicals: List[int],
) -> Chem.Mol:
    xyz_block = build_xyz(coords, atoms)
    rdmol = Chem.RWMol(Chem.MolFromXYZBlock(xyz_block))
    for bond_start, bond_end, bond_order in bonds:
        rdmol.AddBond(bond_start, bond_end, bond_list[bond_order])
    for atom, charge, spin in zip(
        rdmol.GetAtoms(), formal_charges, formal_num_radicals
    ):
        atom.SetFormalCharge(charge)
        atom.SetNumRadicalElectrons(spin)
    rdmol = rdmol.GetMol()
    Chem.SanitizeMol(rdmol)
    return rdmol


def recover_rdmol_from_snapshot(snapshot: Snapshot) -> Chem.Mol:
    return recover_rdmol(
        coords=snapshot.coords,
        atoms=snapshot.atoms,
        bonds=snapshot.bonds,
        formal_charges=snapshot.formal_charges,
        formal_num_radicals=snapshot.formal_num_radicals,
    )



def build_xyz(
    coords: List[List[float]],
    atoms: List[str],
):
    xyz_block = (
        f"{len(coords)}\n"
        + "\n"
        + "\n".join(
            [
                f"{Chem.Atom(atom).GetSymbol():10s}{x:10.5f}{y:10.5f}{z:10.5f}"
                for atom, (x, y, z) in zip(atoms, coords)
            ]
        )
    )

    return xyz_block


def build_xyz_from_snapshot(snapshot: Snapshot):
    return build_xyz(
        coords=snapshot.coords,
        atoms=snapshot.atoms,
    )

def smiles_to_formula_dict(smi: str):
    mol = Chem.AddHs(Chem.MolFromSmiles(smi))
    formula_dict = {element: 0 for element in elements_in_pt}
    for atom in mol.GetAtoms():
        symbol = atom.GetSymbol()
        formula_dict[symbol] += 1
    return {symbol: count for symbol, count in formula_dict.items() if count > 0}
