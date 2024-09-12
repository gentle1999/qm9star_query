<!--
 * @Author: TMJ
 * @Date: 2024-05-24 14:42:44
 * @LastEditors: TMJ
 * @LastEditTime: 2024-09-08 20:47:00
 * @Description: 请填写简介
-->
# Download and Extract QM9 Dataset

You can download the QM9 dataset from [here](https://figshare.com/articles/dataset/Data_for_6095_constitutional_isomers_of_C7H10O2/1057646?backTo=/collections/_/978904).

After downloading the dataset, you can extract it using the following steps:

- Uncompress the downloaded file and rename the extracted folder to `qm9`.

- run `python parse_qm9.py`

This script will parse the QM9 dataset and create two csv files: `qm9_local.csv` and `qm9_global.csv`.

```raw
Ramakrishnan, Raghunathan; Dral, Pavlo; Rupp, Matthias; Anatole von Lilienfeld, O. (2014). Quantum chemistry structures and properties of 134 kilo molecules. figshare. Collection. https://doi.org/10.6084/m9.figshare.c.978904.v5
```
