---
layout: default
title: S26 Wheat
nav_order: 3
has_toc: false
---

# Spring 2026

We will reproduce the phylogenetic analyses of [Pervasive hybridizations in the history of wheat relatives](https://www.science.org/doi/10.1126/sciadv.aav9188) by Glemin et al (2019).

## Software

- RAxML
- SuperTriplets
- ASTRAL
- Julia
  - SNaQ
  - PhyloPlots
- HyDe
- R
  - ape, phangorn, ggtree, MSCQuartets

## Schedule 2026

| Week | Session | Topic | Pre-class work | Lecture notes | Homework | 
| :---: | :---:   | :---: | :---:         | :---: | :---: | 
| 0 | 01/23 | Canceled due to extreme cold weather
| 1 | 01/30 | Introduction and reproducibility practices | | [notes](https://solislemuslab.github.io/phylo-practicum/notes/1-intro-reproducibility.html) | Set-up local folder for the class ([HW](https://github.com/solislemuslab/phylo-practicum/blob/main/notes/1-intro-reproducibility.md#homework)) |
| 2 | 02/06 | Paper discussion | Read [Glemin et al, 2019](https://www.science.org/doi/10.1126/sciadv.aav9188); Optional reading [Marcussen et al, 2014](https://www.science.org/doi/full/10.1126/science.1250092) | | [notes](https://solislemuslab.github.io/phylo-practicum/glemin-wheat/code/02-paper-discussion.html)
| 3 | 02/13 | Goal of the analyses, required software and data | | [notes](https://solislemuslab.github.io/phylo-practicum/glemin-wheat/code/03-data-software.html) | Make sure all software is properly installed in your computer |
| 4 | 02/20 |Gene tree inference | | [notes](https://solislemuslab.github.io/phylo-practicum/glemin-wheat/code/04-gene-trees.html) | Run RAxML on all genes |
| 5 | 02/27 | Species tree: supermatrix (full concatenation) | | [notes](https://solislemuslab.github.io/phylo-practicum/glemin-wheat/code/05-species-tree-supermatrix-full.html) | Finish the RAxML analyses on your own and visualize the results; Optional: run the script to concatenate genes yourself |
| 6 | 03/06 | Species tree: supermatrix (10Mb sliding window) | | [notes](https://solislemuslab.github.io/phylo-practicum/glemin-wheat/code/06-species-tree-supermatrix-10mb.html) | Finish the RAxML analyses on your own and visualize the results; Optional: run the script to create the 10Mb windows yourself |
| 7 | 03/13 | Species tree: supertree and coalescent-based (new analysis) | | [notes](https://solislemuslab.github.io/phylo-practicum/glemin-wheat/code/07-species-tree-supertree-coal.html) | Finish the ASTRAL analyses |
| 8 | 03/20 | Species tree results (Figure 1) | Install and read about [ggtree](https://yulab-smu.top/treedata-book/) | [notes](https://solislemuslab.github.io/phylo-practicum/glemin-wheat/code/08-species-tree-visualizations.html)
| 9 | 03/27 | Species network inference (new analysis + Figure 5) | | [notes](https://solislemuslab.github.io/phylo-practicum/glemin-wheat/code/09-species-network.html) | Leave the snaq job running in the background | 
|  | 04/03 | Spring break
| 10 | 04/10 | Hybrid tests: HyDe | | [notes](https://solislemuslab.github.io/phylo-practicum/glemin-wheat/code/10-hybrid-detection-hyde.html) | Leave HyDe analyses for 10Mb windows running in the background |
| 11 | 04/17 | Hybrid tests: MSCQuartets and visualizations (Figures 3-4) | | [notes](https://solislemuslab.github.io/phylo-practicum/glemin-wheat/code/11-hybrid-detection-mscquartets.html) 
| 12 | 04/24 | Interpreting hybridization results 
| 13 | 05/01 | Open question: other analyses
|  | 05/04 | Final reproducible script due


### More details

See list of topics, grading and academic policies in the [syllabus](https://github.com/solislemuslab/phylo-practicum/blob/main/syllabus.tex)
