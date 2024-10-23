<!--
 * @Author: TMJ
 * @Date: 2024-04-29 09:59:49
 * @LastEditors: TMJ
 * @LastEditTime: 2024-10-23 10:15:33
 * @Description: 请填写简介
-->
# qm9star_query

A SQLModel-based repository dedicated to helping users access the PostgreSQL-based qm9star database more easily in a Python environment.

This is a repository for paper *"[QM9star, two million DFT-computed equilibrium structures for ions and radicals with atomic information](https://www.nature.com/articles/s41597-024-03933-6)"*.

## Usage

This repository requires a reasonably deployed QM9star database to run. For information on how to deploy a QM9star database, please refer to the [download_and_deploy_qm9star](tutorial/1-download_and_deploy_qm9star.md).

Once you have deployed correctly and checked network connectivity, you can refer to the [query_example](tutorial/2-query_example.ipynb) to run queries.

## Installation

### For users who only want to use the functions of connecting to databases and downloading datasets in this project, you can install the package following the steps below

```bash
git clone https://github.com/gentle1999/qm9star_query.git
cd qm9star_query
pip install poetry # if you don't have poetry installed
poetry install
```

### A demonstration guide on how to train neural network potential functions using the QM9star dataset is also provided in this project, and if you want to use these functions, you need to refer to the following steps

```bash
poetry install -E dl
```

If your cuda version not matches 12.1, you need to remove the dependencies of pyg-lib and other related packages. And then install them again with the correct cuda version. You can find the `whl` list on [pyg-lib](https://data.pyg.org/whl/index.html)

```bash
poetry remove pyg-lib torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric
poetry add https://data.pyg.org/whl/torch-2.3.0%2Bcu121.html # Use correct cuda version
```

**Note**: If you excute `poetry install` without `--E dl` again, the extra dependencies will be removed.

### Failure Solution

- DIG dependency conflict
  
The `DIG` package contains a dependency called `rdkit-pypi`, which may overwrite the original higher version of rdkit when installing, if you encounter this problem, you can use the following methods to solve it.

```bash
poetry remove rdkit
poetry add rdkit
```

Poetry will consider these to be two packages, so it will check that they both exist, but we want the higher version of rdkit to override the lower one.

- Poetry stuck at pending

Sometimes Poetry's dependency resolution gets stuck in hellish wait times, which can be due to network or other reasons. In this case, you can try installing the dependency directly using the following command

```bash
pip install .
pip install .[dl] # If you want to use the dl functions
```

## How to cite

```bibtex
@article{tangQM9starTwoMillion2024a,
  title = {{{QM9star}}, Two Million {{DFT-computed}} Equilibrium Structures for Ions and Radicals with Atomic Information},
  author = {Tang, Miao-Jiong and Zhu, Tian-Cheng and Zhang, Shuo-Qing and Hong, Xin},
  year = {2024},
  month = oct,
  journal = {Scientific Data},
  volume = {11},
  number = {1},
  pages = {1158},
  issn = {2052-4463},
  doi = {10.1038/s41597-024-03933-6},
  urldate = {2024-10-22},
  langid = {english}
}
```
