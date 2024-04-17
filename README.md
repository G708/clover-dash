# clover-dash

## 0. ChangeLog
Please see [ChangeLog.md](ChangeLog.md)

## 1. Overview
`Clover` is tool for prioritising rare genes in a differentially expressed gene (DEG) list. We used this tool to rank DEGs from bulk RNA-seq analysis, but any gene list with an FDR value (statistically significant value of differentially expressed) is applicable. 

## 2. Installation

Everything is contained in a docker image. To install docker, please see [here](https://docs.docker.com/get-docker/).

```bash
docker pull g7o8/clover-dash
```

## 3. Usage
To run the docker image, please use the following command:

```bash
docker run --rm -p 8050:8050 clover-dash
```

Then, open your browser and go to [http://localhost:8050/](http://localhost:8050/). 
After that, follow the instruction to run `Clover`.

## 4. Input
The input file is eather CSV or TSV file with the gene name (HGNC Symbol) or id (Entrez Gene ID, Ensembl Gene ID) and FDR columns. The header is required.

## 5. Function
In the `clover-dash` dashboard, you can do the following:

### 5.1 Home page
- Run `Clover` with your input file and calculate the `Glint`, `Dowsing`, `Treasure Hunt`, and `Ropeway` for each gene.
- Download the result as a csv file.
- Generate WordClouds for each ranking.

### 5.2 Data Sources page
- Interact with the `Clover` database.
	i.e.) Exproler interested gene in `DE prior`, `Gini index`, and `number of publications` distribution plots.

## 5. Output
The output file is a csv file with the gene name (HGNC Symbol), gene id (Entrez Gene ID, Ensembl Gene ID), FDR, `Glint`, `Dowsing`, `Treasure Hunt`, and `Ropeway` columns.  Also able to download plots using plotly function.

## 6. Citation
If you use `Clover` or `clover-dash`, please cite the following:

> Oba GM, Nakato R. Clover: An unbiased method for prioritizing differentially expressed genes using a data-driven approach. Genes Cells. 2024 Apr 11. doi: [10.1111/gtc.13119](https://doi.org/10.1111/gtc.13119). Epub ahead of print. PMID: 38602264.
