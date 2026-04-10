---
layout: default
title: 09 Species network
parent: S26 Wheat
nav_order: 8
---

# Species network

## Creating input files

We have the estimated gene trees (`04-all-gene-trees.tre`) and the mapping of individuals to species (`07-species_mapping.txt`). We want to run [SNaQ](https://juliaphylo.github.io/SNaQ.jl/stable/man/multiplealleles/) on multiple alleles to estimate the species network at species level (13 wheat species and 4 outgroups).

We also have a starting species tree at species level (`07-species-tree.tre`).

Now, in Julia, in the `code` folder:
```julia
using PhyloNetworks
using SNaQ
using CSV, DataFrames

mappingfile = CSV.read("../results/07-species_mapping.txt", DataFrame; header=false, delim=' ')
```

Note that we have this file as column1=individual and column2=species, and we need the opposite for SNaQ. We also need the columns to have names "species" and "individual".

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

Now we read the gene trees and compute CF table:
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

## Running SNaQ to infer phylogenetic network

First, we want to create a subfolder `snaq` in `results.

We want to open a Julia session with multithreads. So, we need to type in the terminal (in the `code` folder):
```
julia -t 2
```

And now inside Julia:

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
Note that this command will take several days to run, so we should leave it running somewhere in the background.

We get:
```
MaxNet is (Ae_sharonensis,Ae_longissima,(Ae_bicornis,(Ae_searsii,((Ae_tauschii,(((Ae_uniaristata,Ae_comosa)1:0.4918206502664954,(Ae_caudata,Ae_umbellulata)1:0.13449338165653227)1:0.00911821493436927,((T_boeoticum,T_urartu)1:1.6460105085783057,(H_vulgare,((Ae_speltoides,Ae_mutica)1:0.07124470208266999)#H26:0.14159810198824307::0.7563186990617421)1:0.1869824746969994)1:0.46325640725730144)0.99651:0.06048455134529327):0.16788568790821257,#H26:0.0::0.2436813009382579):0.45932787904385297)1:0.9296082436533977)1:0.5926597507029276)1; 
with -loglik 201.8386327450107 
from run number 85
```

And we can plot with:
```julia
using PhyloPlots
# net = readnewick("(Ae_sharonensis,Ae_longissima,(Ae_bicornis,(Ae_searsii,((Ae_tauschii,(((Ae_uniaristata,Ae_comosa)1:0.4918206502664954,(Ae_caudata,Ae_umbellulata)1:0.13449338165653227)1:0.00911821493436927,((T_boeoticum,T_urartu)1:1.6460105085783057,(H_vulgare,((Ae_speltoides,Ae_mutica)1:0.07124470208266999)#H26:0.14159810198824307::0.7563186990617421)1:0.1869824746969994)1:0.46325640725730144)0.99651:0.06048455134529327):0.16788568790821257,#H26:0.0::0.2436813009382579):0.45932787904385297)1:0.9296082436533977)1:0.5926597507029276)1;")
plot(net, showedgenumber=true)
```

We want to root on the outgroup:
```julia
rootonedge!(net, 16)
rotate!(net,22)
rotate!(net,23)
rotate!(net,-6)
rotate!(net,12)
rotate!(net,11)
plot(net, showgamma=true)
```

Note that the backbone tree (the major tree) matches the one estimated by full concatenation and astral. To compare to Figure 5, we need to consider the following two clades:
- _Comopyrum_ clade includes Aegilops comosa and Aegilops uniaristata.
- _Sitopsis_ clade includes Aegilops bicornis, Aegilops longissima, Aegilops searsii, and Aegilops sharonensis.

SNaQ network finds a hybridization from the ancestor of Sitopsis into the ancestor of Ae mutica and Ae speltoides which does not appear in Figure 5. The closest is hybridization 3.

Let's try to use the same colors as in Figure 5:

```julia
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

[Note this still does not work]