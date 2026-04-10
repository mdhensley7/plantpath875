---
layout: default
title: 05 Species tree supermatrix (full)
parent: S26 Wheat
nav_order: 4
---

# Species tree via concatenation

There will be two types of concatenation:
- full concatenation
- 10Mb windows

## Full concatenation

The authors already provide the fully concatenated fasta file in `FullConcatenation_OneCopyGenes.zip` and when you unzip, you get `triticeae_allindividuals_OneCopyGenes.fasta`. We will run RAxML on this file following the details in the paper: "We inferred the phylogeny from this supermatrix with RAxML v8 using the GTR+Γ4 model and the fast-bootstrap option".

Note that RAxML will save output files in the folder where the data is, so we will run the command in the `data/Wheat_Relative_History_Data_Glemin_et_al` folder:

```
raxml-ng --msa triticeae_allindividuals_OneCopyGenes.fasta --model GTR+G4
```

Note that this will take ~24 hours to run and after that, we move the output files to the `results` folder:

```
cd ../../results/RAxML/
mkdir full-concatenation
cd ../../data/Wheat_Relative_History_Data_Glemin_et_al
ls ## to check files are there
mv *.raxml* ../../results/RAxML/full-concatenation
```

### Creating our own concatenated file

We could practice the process of concatenating all the sequence files in `OneCopyGenes`. The specific code can be found in `06-make-supermatrix.R`.
Briefly, we first create an empty sequence file for each taxon. Then we read in each gene and append the seqeunces to the taxon sequence files. At the end of this we should have a fully populated sequence for each taxon; we just append paste these together in a file and we have our concatenated matrix. 

Our manual concatentation file is saved in a folder called `OneCopyGenes-supermatrix` and is called `manual_supermatrix.fasta`.

As a check for correctness, we could then run RAxML on this concatenation file and it should yield similar results to the published concatenation file.

### Visualization

We open R in the `results/RAxML/full-concatenation/` folder:

```r
library(ape)
library(phangorn)
library(phytools)

tre = read.tree(file="triticeae_allindividuals_OneCopyGenes.fasta.raxml.bestTree")
plot(tre)
nodelabels()
```

Note that we need to root at the outgroup clade: `H_vulgare_HVens23`, `Ta_caputMedusae_TB2`, `Er_bonaepartis_TB1`, `S_vavoilovii_Tr279` which corresponds to node=51.

```r
rtre = root(tre,node = 51, resolve.root=TRUE)
plot(ladderize(rtre))
```

We can compare to the one provided by the authors: `MLtree_OneCopyGenes.tree`:

```r
tre2 = read.tree(file="../../../data/Wheat_Relative_History_Data_Glemin_et_al/MLtree_OneCopyGenes.tree")
plot(tre2)
rtre2 = root(tre2,node = 51, resolve.root=TRUE)
plot(ladderize(rtre2))
```

We can also calculate the RF distance between our full concatenation tree and theirs:

```r
library(phangorn)
RF.dist(tre,tre2) ## 0
```