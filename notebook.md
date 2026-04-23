# Phylogenetic Practicum

This is the script I will be writing to execute the walk through of the phylogenetic process of Glemin et al. 2018

The paper uses an incredible amount of genetic information to make inferences on the phylogenetic history of wheat genomes. Using these methods, the scientists were able to produce strong evidence towards the hybridization event happening between the A genome and the genome of a wild species of wheat Aegilops mutica. This is evidence against the previously accepted notion that the hybridization event happened between the A and B genome.

## Needed software

### RAX-ML
```zsh
cd software/raxml-ng_v1.2.2_macos/ ## you need to modify to your own path
ls ## check the raxml-ng executable is there
cp raxml-ng /usr/local/bin
```

### Supertriplets
```zsh
java -jar -Xmx500m ~/software/supertriplets/SuperTriplets_v1.1.jar newick_file.nwk outfile
```
Download placed in Documents/coding_tools

### ASTRAL
```zsh
conda config --add channels bioconda
conda install aster
which wastral #Outputs where it was installed
wastral #to test if it works
```

### Julia packages
```zsh
curl -fsSL https://install.julialang.org | sh
juliaup add release #installs julia
julia #starts julia in the terminal
    > add PhyloNetworks
    > add SNaQ
    > add PhyloPlots
    > add CSV
    > add DataFrames
    exit() 
    # exits julia
```

### HyDe
```zsh
git clone https://github.com/pblischak/HyDe.git
# move HyDe folder to repository
cd HyDe
python3 -m pip install -r requirements.txt
python3 -m pip install .
```

### R
In R, these packages were installed:
    > install.packages("ape")
    > install.packages("phangorn")
    > install.packages("BiocManager")
    > BiocManager::install("remotes")
    > BiocManager::install("YuLab-SMU/treedataverse")
    > install.packages("MSCquartets")
    > install.packages("phytools")
    > install.packages("ggplot2")

## 04 Gene tree estimation

In class we used the code to run RAxML on 10 genes with this code

```zsh
cd glemin-wheat/data/Wheat_Relative_History_Data_Glemin_et_al

mkdir OneCopyGenes-trimmed
cd OneCopyGenes
ls | head -n10 | xargs -I {} cp "{}" ../OneCopyGenes-trimmed
#This last line copies the first 10 genes in 'Wheat_Relative_History_Data_Glemin_et_al' to the new folder
```

To automate this further, Claudia/whoever else coded a bash script called '04-raxml.sh'

Definitely check out this to learn how to automate with bash: https://learnxinyminutes.com/bash/

So, now we have the trimmed folder, we can run the bash script on the folder to output genetrees from raxml

Here is the bash script:
```zsh
#!/bin/bash

DATADIR="../data/Wheat_Relative_History_Data_Glemin_et_al/OneCopyGenes-trimmed"

mkdir ../results/
mkdir ../results/RAxML/

for file in "$DATADIR"/*; do
    raxml-ng --msa $file --model GTR+G4
    mv ${file}**raxml** ../results/RAxML/
done
```

To run it:
```zsh
cd glemin-wheat/code
./04-raxml.sh
```

This produced 8 output files for each of the 10 genes
```zsh
cd ../results/RAxML
ls
```

From here, tree analysis was done in R. Go to R markdown file for the analysis walkthrough.

To have all the gene trees run, we must edit '04-raxml.sh' to work on all not just the trimmed folder

```zsh
DATADIR="../data/Wheat_Relative_History_Data_Glemin_et_al/OneCopyGenes-trimmed"
#Change to below
DATADIR="../data/Wheat_Relative_History_Data_Glemin_et_al/OneCopyGenes"
#Save changes and repeat command
cd glemin-wheat/code
./04-raxml.sh
```

This will take about 9 hours to run.

QUESTION: Did we need to delete the first ten genes that were already in the results folder?

ANSWER: Probably not. Might've just gotten overwritten or was put into a different folder lol.

## 05 Species tree super matrix full

Another way to estimate the species tree. But ultimately are inconsistent because of Incomplete Lineage Sorting (ILS). Concatenation is a good way to just visualize the data to get a sense for it. I would be weary about using it for a functional phylogeny.

We can also do concatenation and divide into 10Mb windows to see if the histories of the windows are consistent with one another. Windows can also allow us to pick up psuedo chromosomal differences like introgression, HGT, and other larger scale genetic dynamics. We can also see if there was 1 hybridization event versus multiple. If one window came from genome A and another window came from genome B we would likely say only one clean hybridization event happened. If we are seeing small chunks of windows come from different parents likely this is the product of multiple events.

The concatenated .fasta file is provide by the authors
```zsh
cd glemin-wheat/data/Wheat_Relative_History_Data_Glemin_et_al
raxml-ng --msa triticeae_allindividuals_OneCopyGenes.fasta --model GTR+G4
```

## 06 Species tree via concatenation: 10 Mb sliding windows
Using these windows, we can inspect if different sections of the genomes have different evolutionary histories. Gives us an indication of past introgression events

```zsh
cd Concatenation10Mb_OneCopyGenes
ls | wc -l
    248 #Should out put this number

cd ../../code
zsh 06-raxml-concatenation.sh # this script builds one species tree per file 
```

Making the 10Mb pair windows was done in the R script

## 07 Species tree via supertree
### Generating supertree.tre from supertriplets
```zsh
cd glemin-wheat/results
java -jar ~/software/SuperTriplets_v1.1.jar 04-all_gene_trees.tre 07-supertree.tre
```

Go to Rmd for visualization process

### Generating ASTRAL species tree
```zsh
cd glemin-wheat/results
astral4 -i 04-all_gene_trees.tre -o 07-individual-species-tree-astral4.tre
```
I wasn't able to get this to run and whenever I have run astral I have had to do so within the folder that astral itself is in. I'm not so sure how to go about this step

### THIS IS GOOD TO KNOW
Astral has the ability to create a species tree where it collapses individuals into their designated species using a mapping .txt file

```zsh
cd glemin-wheat/results
astral -i 04-all_gene_trees.tre -a 07-species_mapping.txt -o 07-species-tree-astral4.tre
```

## 10 Detecting hybridization using HYDE

```zsh
from Bio import SeqIO

#read in the fasta format sequence
data_path = "../data/Wheat_Relative_History_Data_Glemin_et_al/"
concat_file = "triticeae_allindividuals_OneCopyGenes.fasta"
records = SeqIO.parse(data_path+concat_file, "fasta")

#convert the output to phylip
count = SeqIO.write(records, "../results/10-triticeae_allindividuals_OneCopyGenes.phylip", "phylip-relaxed")

```

## 11 Hybrid detection with MSCQuartets and Visualization
Find notes in Phylo_Practicum_R.Rmd