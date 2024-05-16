<!--
 * @Author: TMJ
 * @Date: 2024-04-29 09:59:49
 * @LastEditors: TMJ
 * @LastEditTime: 2024-05-16 18:43:48
 * @Description: 请填写简介
-->
# qm9star_query

A SQLModel-based repository dedicated to helping users access the PostgreSQL-based qm9star database more easily in a Python environment.

## Installation

### For users who only want to use the functions of connecting to databases and downloading datasets in this project, you can install the package following the steps below:

```bash
git clone http://10.72.201.58:13000/tmj/qm9star_query.git
cd qm9star_query
pip install poetry # if you don't have poetry installed
poetry install
```
### A demonstration guide on how to train neural network potential functions using the QM9star dataset is also provided in this project, and if you want to use these functions, you need to refer to the following steps:

```bash
poetry install -E dl
```

If your cuda version not matches 12.1, you need to remove the dependencies of pyg-lib and other related packages. And then install them again with the correct cuda version. You can find the `whl` list on [pyg-lib](https://data.pyg.org/whl/index.html)

```bash
poetry remove pyg-lib torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric
poetry add https://data.pyg.org/whl/torch-2.3.0%2Bcu121.html # Use correct cuda version
```
The `DIG` package contains a dependency called `rdkit-pypi`, which may overwrite the original higher version of rdkit when installing, if you encounter this problem, you can use the following methods to solve it.

```bash
poetry remove rdkit
poetry add rdkit
```

Poetry will consider these to be two packages, so it will check that they both exist, but we want the higher version of rdkit to override the lower one.

**Note**: If you excute `poetry install` without `--E dl` again, the extra dependencies will be removed.

## Usage

This repository requires a reasonably deployed QM9star database to run. For information on how to deploy a QM9star database, please refer to the [download_and_deploy_qm9star](tutorial/1-download_and_deploy_qm9star.md).

Once you have deployed correctly and checked network connectivity, you can refer to the [query_example](tutorial/2-query_example.ipynb) to run queries.



