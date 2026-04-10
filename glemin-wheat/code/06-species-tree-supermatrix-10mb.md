---
layout: default
title: 06 Species tree supermatrix (10Mb)
parent: S26 Wheat
nav_order: 5
---

# Species tree via concatenation: 10Mb sliding window

Rather than building one species tree for the fully concatenated sequences, we could create smaller concatenated files (10Mb windows) to assess tree discordance.
The authors provide already the 10Mb sliding window concatenated sequence files in the `Concatenation10Mb_OneCopyGenes.zip` file which unzips into the `Concatenation10Mb_OneCopyGenes` folder:

```
$ cd Concatenation10Mb_OneCopyGenes
$ ls | wc -l
     248
```

In the paper, the authors say:
"Using the Hordeum genome as a reference, we also concatenated genes in 10-Mb windows along chromosomes, obtaining 298 alignments with at least three genes per window.

Among the 298 10-Mb trees, only 248 contained all individuals."

We want to build one species tree per file, so we will use a similar bash script to the one for gene trees (`06-raxml-concatenation.sh`). This script has the flag `--threads 5` to use 5 threads within each raxml job.

Within the `code` folder:
```
./06-raxml-concatenation.sh
```

There are 248 genes, each gene tree estimation took around 140 seconds in my computer (so total would be ~10 hours).

### Making the 10Mb windows ourselves

We can attempt to make the 10MB windows ourselves for analysis. We will use the script `06-make-10Mb-windows.R` to create the 10Mb windows per chromosome. This script uses the gene location mapping given by `MappedOnHordeumChromosomes_OneCopyGenes.txt`. This file maps each gene to a chromosome and a position on that chromosome. Then, for each chromosome, we start at position 1 and concatenate all genes in 10Mb windows. One thing worth noting here is that with our process, we generate 321 windows that have at least three genes in them. It is not clear how our window generation is different from the published generation.

Also interestingly, when trying to concatenate genes, we found that 31 genes have multiple records per individual although the dataset are listed as single copy genes. This creates issues for concatenation and so we remove all individuals with multiple sequences for that gene.

### Visualization

We want to reproduce Figure 1(B) with a densitree with all species trees from 10Mb sliding windows.

We need to be in the `results/RAxML/10Mb-concatenation` folder:

```r
library(ape)
library(phangorn)
library(phytools)
library(ggplot2)

getwd() #Check the working directory. we want to be in the results/RAxML/10Mb-concatenation folder
#setwd("PathTo/results/RAxML/10Mb-concatenation") #replace PathTo with the correct path and run if not in the correct folder

tree_files <-list.files(pattern="\\.raxml.bestTree$") #List all .bestTree files. $ ensures the end of the name

trees<- list() # list with all the trees
class(trees)<- "multiPhylo" #make it a multiphylo object for ease of use with other 

i<-1
for(tree_file in tree_files){ ##go thru each file and read the tree
  trees[[i]]<- read.tree(tree_file)
  i<-i+1
}
```

We need to root all trees in "H_vulgare_HVens23" to reproduce [Figure 1(B)](https://www.science.org/doi/10.1126/sciadv.aav9188):

```r
#re-reroot all our gene trees by the respective outgroup
for(i in 1:length(trees)){
  trees[[i]]<- root(trees[[i]],
                         outgroup = "H_vulgare_HVens23",
                         resolve.root=TRUE)
  trees[[i]]<-chronos(trees[[i]]) ## make ultrametric for nicer densitree
}
```

We will create a consensus parsimony supertree:

```r
st<-superTree(trees)
st<-root(st,"H_vulgare_HVens23",resolve.root = T)
plot(st)
```

Finally, we plot the same density tree as Figure 1B:

```r
densiTree(trees,consensus=st,scaleX=T,type='cladogram', alpha=0.1)
```


We can compare the densitree with the one provided by the authors: `Densitree_OneCopyGenes.nex`. We had issues reading this file into R, so we had to make some minor manual modifications (`Densitree_OneCopyGenes-modified.nex`):
1. Added ; after "begin trees"
2. Had to manually change taxon 0 as 47 (in translate block and all the trees)

```r
trees2 <- read.nexus("../../../data/Wheat_Relative_History_Data_Glemin_et_al/Densitree_OneCopyGenes-modified.nex")

#re-reroot all our gene trees by the respective outgroup
for(i in 1:length(trees2)){
  trees2[[i]]<- root(trees2[[i]],
                         outgroup = "H_vulgare_HVens23",
                         resolve.root=TRUE)
  trees2[[i]]<-chronos(trees2[[i]]) ## make ultrametric for nicer densitree
}

st2<-superTree(trees2)
st2<-root(st2,"H_vulgare_HVens23",resolve.root = T)
plot(st2)

densiTree(trees2,consensus=st2,scaleX=T,type='cladogram', alpha=0.1)
```