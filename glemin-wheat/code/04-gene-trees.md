---
layout: default
title: 04 Gene tree estimation
parent: S26 Wheat
nav_order: 3
---

# Gene Trees

The data started with 13,288 genes which were filtered to 12,959 by discarding trees where the outgroups were not monophyletic (this set was denoted F_i). They renamed each sequence as the species to go from F_i to F_m (F_m^95 only has clades with bootstrap greater than 95).
They used SSIMUL to go from multilabeled trees in F_m (F_m^95) to single labeled trees (denoted F_s and F_s^95 respectively). They pruned isomorphic trees so that there are only now 11,033 gene trees.
Finally, they kept the 8739 gene trees containing at most one sequence per individual (each individual has only one sequence (copy)). This is the data we have.
The zipped folder `IndividualAlignements_OneCopyGenes.zip` contains a folder `OneCopyGenes` with 8739 aligned genes.

## Using RAxML 

The `raxml-ng` command is used to run RAxML and estimate a gene tree from an alignment. `raxml-ng` has many different configurations, models, and parameter settings that can be specified by adding additional arguments to the command. You can use `raxml-ng -h` to see all of the arguments. We will be use RAxML using the default settings and a GTR model with a four category gamma distribution for site variation. For a single gene the command would look like this:
```
raxml-ng --msa T_urartu_Tr309_URA15_Singlet902_simExt_macseNT_noFS_clean.aln --model GTR+G4
```

The `--msa` flag specifies the alignment file that will be used to construct the phylogeny while the `--model` flag specifies the model of sequence evolution. The authors conduct a bootstrap analysis for each gene tree; this can be done with the `--bs-trees` flag. However, to save on computation time, we will not conduct bootstrap analyses.  


## Running RAxML on 10 genes


Since running RAxML on each gene will take some time, we will create a data folder with only 10 genes that we can run in class. The full set will then be run as HW.

We are in the `data/Wheat_Relative_History_Data_Glemin_et_al` folder. We create a subfolder called `OneCopyGene-trimmed` and copy the first 10 genes in this folder.
```
mkdir OneCopyGenes-trimmed
cd OneCopyGenes
ls | head -n10 | xargs -I {} cp "{}" ../OneCopyGenes-trimmed
```

The subfolder `OneCopyGenes-trimmed` now contains the first 10 alignments from `OneCopyGenes`.

We could run RAxML on the terminal directly with the `raxml-ng` executable one by one, but instead we will run it through a bash script so that we can loop over genes and we can move output files to a `results` folder. To automate this process we wrote the bash script called `04-raxml.sh`. If you're interested in using bash to automate some processes, we recommend checking out [Learn X in Y minutes (where X=Bash)](https://learnxinyminutes.com/bash/).

Note that we will not run bootstrap because this was used on previous steps for data filtering and it save computation time.

Now we move to the `code` folder to run the `04-raxml.sh` script.

```
./04-raxml.sh
```

For each gene, we have 8 output files created inside `results/RAxML`:
```
Ae_bicornis_Tr406_BIS2_Contig10132_simExt_macseNT_noFS_clean.aln.raxml.startTree 
Ae_bicornis_Tr406_BIS2_Contig10132_simExt_macseNT_noFS_clean.aln.raxml.reduced.phy 
Ae_bicornis_Tr406_BIS2_Contig10132_simExt_macseNT_noFS_clean.aln.raxml.rba 
Ae_bicornis_Tr406_BIS2_Contig10132_simExt_macseNT_noFS_clean.aln.raxml.mlTrees 
Ae_bicornis_Tr406_BIS2_Contig10132_simExt_macseNT_noFS_clean.aln.raxml.log 
Ae_bicornis_Tr406_BIS2_Contig10132_simExt_macseNT_noFS_clean.aln.raxml.bestTreeCollapsed 
Ae_bicornis_Tr406_BIS2_Contig10132_simExt_macseNT_noFS_clean.aln.raxml.bestTree 
Ae_bicornis_Tr406_BIS2_Contig10132_simExt_macseNT_noFS_clean.aln.raxml.bestModel
```

You can find more details about the output files [here](https://github.com/amkozlov/raxml-ng/wiki/Output:-files-and-settings#output-prefix). 

### Analyzing the results

We will primarily be analyzing the inferred gene trees in R.

First we want to read in each gene tree; for this we will primarily be focusing on the output file with the suffix `raxml.bestTree` which contains the maximum likelihood tree.

In `results/RAxML`:

```r
library(ape)
library(phangorn)
library(phytools)
library(ggplot2)

getwd() #Check the working directory. we want to be in the results/RAxML folder
#setwd("PathTo/results/RAxML") #replace PathTo with the correct path and run if not in the correct folder

tree_files <-list.files(pattern="\\.raxml.bestTree$") #List all .bestTree files. $ ensures the end of the name

gene_trees<- list() # list with all the trees
class(gene_trees)<- "multiPhylo" #make it a multiphylo object for ease of use with other 

i<-1
for(tree_file in tree_files){ ##go thru each file and read the tree
  gene_trees[[i]]<- read.tree(tree_file)
  i<-i+1
}
```

Now we have all of the gene trees in our object named `gene_trees`.

We may want some basic checks for correctness of the dataset. In the paper, they filtered data by being able to root the gene tree from these species in order:  H_vulgare, Er_bonaepartis, S_vavilovii, and Ta_caputMedusae. We can confirm that each gene tree has at least one of these taxa and re-root in R with the following code:

```r
#Find the appropriate root taxon
root_taxa <- c("H_vulgare_HVens23", "Er_bonaepartis_TB1", "S_vavilovii_Tr279", "Ta_caputMedusae_TB2")

# Extract the first matching species for each tree
gene_tree_outgroup<- rep(NA,length(gene_trees))
for(i in 1:length(gene_trees)){
  gene_tree <- gene_trees[[i]]
  found_taxa <- root_taxa[root_taxa %in% gene_tree$tip.label]
  
  # Return the first one if it exists
  if (length(found_taxa) > 0) {
    gene_tree_outgroup[i]<-found_taxa[1]
  }
}

#check if any gene trees don't have an outgroup taxon
any(is.na(gene_tree_outgroup)) ## should return FALSE

#re-reroot all our gene trees by the respective outgroup
for(i in 1:length(gene_trees)){
  gene_trees[[i]]<- root(gene_trees[[i]],
                         outgroup = gene_tree_outgroup[i],
                         resolve.root=TRUE)
  gene_trees[[i]]<-chronos(gene_trees[[i]]) ## make ultrametric for nicer densitree
}
```

### Visualizing the trees

We can plot the gene trees with the `plot()` command:

```r
#plot(gene_trees) to plot all gene trees sequentially
plot(gene_trees[[2]]) # plots the second gene tree
```

It's important to understand the structure of our data and how filtering choices affect downstream methods. Our dataset currently contains only genes with at most one copy per individual (i.e., single-copy genes). Many genes nevertheless lack some taxa — not every taxon appears in every gene — which makes it harder to summarize and visualize species relationships. A common solution is to restrict the data to complete records (for example, keep only genes that include all individuals, or keep only individuals that appear on all genes). However, supertree methods can handle missing taxa. In any case, we should quantify how often each taxon (or individual) is present across genes:

```r
# see which genes have which taxa
all_labels <- unlist(lapply(gene_trees, function(x) x$tip.label)) ##count how often each individual appears
df <- as.data.frame(table(all_labels) / length(gene_trees)) #organize as a nice data frame for plotting

ggplot(df, aes(x = all_labels, y = Freq)) +
  geom_col() +
  labs(x = "Individual", y = "Proportion")+
  theme(axis.text.x = element_text(angle = 90))
```

In our set of 10 genes it appears that most individuals seem well represented with the exception of the T_boeoticum individuals. If we were using methods that could not account for missing taxa, these results that indicate that we may want to drop T_boeoticum as a species or we may need to aggregate individuals at the species level.

However, for supertree methods we can use the dataset as is. We will explore supertree methods more later in the course but we can apply a simple maximum parsimony approach to create a supertree from all our genes to get a sense of the overall signal from the gene trees.

```r
st<-superTree(gene_trees)
st<-root(st,"H_vulgare_HVens23",resolve.root = T)
plot(st)
```

From here we can see that individuals within a given species  generally create a monophyletic group; this an indicator that we would probably be fine aggregating our data at the species level if we wanted to use methods that don't handle individual-level sampling or we wanted to aggregate our data to deal with the missing taxa across genes.

We can additionally try to plot all of the genes as a densitree plot, a plot where all the gene tree topologies are overlaid over one another to give a high-level cloud of all the signal

```r
densiTree(gene_trees,consensus=st,scaleX=T,type='cladogram', alpha=0.05)
```

This plot shows substantial conflict among genes. This conflict may partly reflect technical issues caused by missing taxa across genes, but it could also represent genuine biological discordance (for example, due to incomplete lineage sorting or gene flow). To improve interpretability, we could either aggregate samples at the species level or restrict the analysis to taxa present in all genes. We try the latter approach next.

```r
common_tips <- Reduce(
  intersect,
  lapply(gene_trees, function(tr) tr$tip.label)
)

length(common_tips) ## 6

trees_pruned <- lapply(
  gene_trees[1:10],
  function(tr) drop.tip(tr, setdiff(tr$tip.label, common_tips))
)

## to remove NULLs:
## trees_pruned <- trees_pruned[!sapply(trees_pruned, is.null)]

densityTree(trees_pruned,use.edge.length=FALSE,type="cladogram",nodes="centered")
```

From here we can see that this approach loses a lot of information (taxa), and this is only when using 10 genes! Even fewer (if any) taxa will have complete records across all sampled genes. This highlights the difficulties of working with empirical datasets and how care is needed when filtering and subsetting your data while trying to maintain signal.

For more information on density trees, you can see this [phytools blog](https://blog.phytools.org/2017/04/slanted-phylogram-cladogram-densitytree.html).


Now, we want to compare the ML trees for each of the 20 RAxML runs (in the `.mlTrees` file). For this, we will do a densitree. This can help us visualize the best tree across each run. With bootstrap analyses, this visualization could illustrate uncertainty across replicates.

```r
trees = read.tree(file="Ae_bicornis_Tr406_BIS2_Contig10132_simExt_macseNT_noFS_clean.aln.raxml.mlTrees")

rtrees <- lapply(trees, function(tr) {
  root(tr, outgroup = "H_vulgare_HVens23", resolve.root = TRUE)
})
```

Plot the densiTree (before and after rooting):
```r
densityTree(trees,type="cladogram",nodes="intermediate")
densityTree(rtrees,type="cladogram",nodes="intermediate")
```

Also if we don't care about differences in branch lengths and we want to focus on differences in topology:
```r
densityTree(trees,use.edge.length=FALSE,type="cladogram",nodes="centered")
densityTree(rtrees,use.edge.length=FALSE,type="cladogram",nodes="centered")
```


## Running RAxML on all the genes

We need to modify the `04-raxml.sh` script so that it loops over all the genes, not just the 10 genes. In the script, we need to change the line:
```
DATADIR="../data/Wheat_Relative_History_Data_Glemin_et_al/OneCopyGenes-trimmed"
```
for
```
DATADIR="../data/Wheat_Relative_History_Data_Glemin_et_al/OneCopyGenes"
```

Then, inside the `code` folder, we run the `04-raxml.sh` bash script:

```
cd code
./04-raxml.sh
```

This command will take around 9 hours to run. 

We can read the trees into R for similar visualizations (not shown).

In `results/RAxML`:

```r
library(ape)
library(phangorn)

getwd() #Check the working directory. we want to be in the results/RAxML folder

tree_files <-list.files(pattern="\\.raxml.bestTree$") #List all .bestTree files. $ ensures the end of the name

gene_trees<- list() # list with all the trees
class(gene_trees)<- "multiPhylo" #make it a multiphylo object for ease of use with other 

i<-1
for(tree_file in tree_files){ ##go thru each file and read the tree
  gene_trees[[i]]<- read.tree(tree_file)
  i<-i+1
}
```

Note that for the list of all gene trees we want to save them to file for future analyses:

```r
write.tree(gene_trees, file="../04-all_gene_trees.tre")
```

