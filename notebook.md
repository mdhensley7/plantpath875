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


## 08 Species tree visualizations
Find notes in Phylo_Practicum_R.Rmd

## 09 Species Network
Using SNaQ and PhyloNetworks in Julia to do species network analysis with our estimated gene trees
    - We will run SNaQ on multiple alleles to estimate species network from 13 wheat species and 4 outgroups
```zsh
cd glemin-wheat/code
```

In terminal run "julia" to open Julia

```julia
using PhyloNetworks
using SNaQ
using CSV, DataFrames

mappingfile = CSV.read("../results/07-species_mapping.txt", DataFrame; header=false, delim=' ')
```
Rotating columns to organize data in a readable manner

```julia
rename!(mappingfile, :Column1 => :individual)
rename!(mappingfile, :Column2 => :species)

select!(mappingfile,[:species, :individual])

## We want to remove 3 of the 4 outgroups to simplify the analysis:
## We keep `H_vulgare_HVens23`, 
## We remove `Ta_caputMedusae_TB2`, `Er_bonaepartis_TB1`, `S_vavilovii_Tr279`
filter(row -> row.species in ["Ta_caputMedusae", "Er_bonaepartis", "S_vavilovii"], mappingfile)
size(mappingfile) ## (47,2)

mappingfile = filter(row -> !(row.species in ["Ta_caputMedusae", "Er_bonaepartis", "S_vavilovii"]), mappingfile)
size(mappingfile) ## (44, 2)

CSV.write("../results/09-species_mapping.csv", mappingfile)

## mappingfile = CSV.read("../results/09-species_mapping.csv", DataFrame)
taxonmap = Dict(r[:individual] => r[:species] for r in eachrow(mappingfile)) # as dictionary
```

Read genes trees and compute CF table

```julia
trees = readmultinewick("../results/04-all_gene_trees.tre")
length(trees) ## 8708


for gt in trees
  for badtip in ["Ta_caputMedusae_TB2", "Er_bonaepartis_TB1", "S_vavilovii_Tr279"]
    if badtip in tiplabels(gt)
      deleteleaf!(gt, badtip)
    end
  end
end


writemultinewick(trees, "../results/09-all_gene_trees_snaq.tre")

## trees = readmultinewick("../results/09-all_gene_trees_snaq.tre")

## creating CF table:
df_sp = tablequartetCF(countquartetsintrees(trees, taxonmap; showprogressbar=false)...);
keys(df_sp)  # columns names
CSV.write("../results/09-tableCF_species.csv", df_sp); 
```
Running SNaQ to infer phylogenetic network
```zsh
julia -t 2 #Opens julia with multithreads
```

```julia
using Distributed
addprocs(4)

@everywhere using PhyloNetworks
@everywhere using SNaQ

## read table of CF
d_sp = readtableCF("../results/09-tableCF_species.csv"); # "DataCF" object for use in snaq!
#read in the species tree from ASTRAL as a starting point
T_sp = readnewick("../results/07-species-tree-astral4.tre")

net = snaq!(T_sp, d_sp, runs=100, Nfail=200, filename= "../results/snaq/09-snaq-h1",seed=8485);
```

Plot with
```julia
using PhyloPlots
# net = readnewick("(Ae_sharonensis,Ae_longissima,(Ae_bicornis,(Ae_searsii,((Ae_tauschii,(((Ae_uniaristata,Ae_comosa)1:0.4918206502664954,(Ae_caudata,Ae_umbellulata)1:0.13449338165653227)1:0.00911821493436927,((T_boeoticum,T_urartu)1:1.6460105085783057,(H_vulgare,((Ae_speltoides,Ae_mutica)1:0.07124470208266999)#H26:0.14159810198824307::0.7563186990617421)1:0.1869824746969994)1:0.46325640725730144)0.99651:0.06048455134529327):0.16788568790821257,#H26:0.0::0.2436813009382579):0.45932787904385297)1:0.9296082436533977)1:0.5926597507029276)1;")
plot(net, showedgenumber=true)

##---To root on the outgroup and color coordinate---#
rootonedge!(net, 16)
rotate!(net,22)
rotate!(net,23)
rotate!(net,-6)
rotate!(net,12)
rotate!(net,11)
plot(net, showgamma=true)

using DataFrames

tipnodes = [n.number for n in net.node if n.leaf]
tipnames = [n.name for n in net.node if n.leaf]

tipcolors = Dict(
    "T_urartu" => "darkolivegreen",
    "T_boeoticum" => "darkolivegreen",
    "Ae_comosa" => "chocolate",
    "Ae_uniaristata" => "chocolate",
    "Ae_caudata" => "khaki",
    "Ae_umbellulata" => "gold",
    "Ae_tauschii" => "red",
    "Ae_longissima" => "mediumorchid",
    "Ae_sharonensis" => "mediumorchid",
    "Ae_bicornis" => "mediumorchid",
    "Ae_searsii" => "mediumorchid",
    "Ae_mutica" => "dodgerblue",
    "Ae_speltoides" => "navy"
)

colors = [get(tipcolors, name, "black") for name in tipnames]

nodelabel = DataFrame(
    number = tipnodes,
    label = tipnames,
    nodelabelcolor = colors
)

plot(net, nodelabel = nodelabel)
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