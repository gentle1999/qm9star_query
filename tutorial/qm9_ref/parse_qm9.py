from glob import glob
import pandas as pd
import os

def parse_qm9(file_path:str):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    atom_num = int(lines[0].split()[0])
    tag, index, A, B, C, mu, alpha, homo, lumo, gap, r2, zpve, U0, U, H, G, Cv = lines[1].split()
    atoms = []
    for i in range(atom_num):
        atom, x, y, z, mulliken_charge = lines[i+2].split()
        try: 
            fx = float(x) 
        except: 
            fx = 0.0
        try: 
            fy = float(y) 
        except: 
            fy = 0.0
        try: 
            fz = float(z)
        except: 
            fz = 0.0
        try:
            mc = float(mulliken_charge)
        except: 
            mc = 0.0
        atoms.append([atom, fx, fy, fz, mc])
    return atoms, float(A), float(B), float(C), float(mu), float(alpha), float(homo), float(lumo), float(gap), float(r2), float(zpve), float(U0), float(U), float(H), float(G), float(Cv)

files = glob('qm9\*.xyz')
total_df_1 = []
total_df_2 = []
for file in files:
    try:
        atoms, A, B, C, mu, alpha, homo, lumo, gap, r2, zpve, U0, U, H, G, Cv = parse_qm9(file_path=file)
    except:
        print("Error in file:", file)
    name = os.path.basename(file).split(".")[0]
    df_1 = pd.DataFrame(atoms, columns=['atom', 'x', 'y', 'z', "mulliken_charge"])
    df_1["name"] = name
    df_2 = pd.DataFrame([[A, B, C, mu, alpha, homo, lumo, gap, r2, zpve, U0, U, H, G, Cv]], columns=['A', 'B', 'C', 'mu', 'alpha', 'homo', 'lumo', 'gap', 'r2', 'zpve', 'U0', 'U', 'H', 'G', 'Cv'])
    df_2["name"] = name
    total_df_1.append(df_1)
    total_df_2.append(df_2)

local_df = pd.concat(total_df_1)
local_df.to_csv('qm9_local.csv', index=False)
global_df = pd.concat(total_df_2)
global_df.to_csv('qm9_global.csv', index=False)