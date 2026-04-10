---
layout: default
title: 10 Hybrid detection with HyDe
parent: S26 Wheat
nav_order: 9
---

# Hybrid detection with HyDe

We can use HyDe to run a series of hytpothesis tests among rooted triplets for signal of hybridization.
We will be following the tutorial [here](https://hybridization-detection.readthedocs.io/analyze.html).
HyDe is available in Python. From the terminal you can open Python with `python3` or `python` (but this may open an older installation). We work on the `code` folder.

## Data Preparation for running HyDe

HyDe needs the sequence data in `Phylip` format, however, our sequences are in `fasta` format. Thus, we will need to convert our sequences to `Phylip` format. We can do this in Python by using the BioPython module.
If BioPython is not installed you can run the command `pip3 install BioPython` in the terminal.

```python
from Bio import SeqIO

#read in the fasta format sequence
data_path = "../data/Wheat_Relative_History_Data_Glemin_et_al/"
concat_file = "triticeae_allindividuals_OneCopyGenes.fasta"
records = SeqIO.parse(data_path+concat_file, "fasta")

#convert the output to phylip
count = SeqIO.write(records, "../results/10-triticeae_allindividuals_OneCopyGenes.phylip", "phylip-relaxed")
```

Additionally we need a mapping file that maps individuals to their respective species. When performing our coalescent analysis, we created the mapping file `07-species-mapping.txt` which is in the exact format that we need.


## Running HyDe on the full concatenation

Now that we have all the components from the terminal we can run `run_hyde.py`. Note that this file was downloaded and set as executable in the PATH when we installed HyDe. You can check you have it by simply typing `run_hyde.py` anywhere in the terminal.
 
For this command, you need to be in the `code` folder:
```
run_hyde.py -i ../results/10-triticeae_allindividuals_OneCopyGenes.phylip -m ../results/07-species_mapping.txt -o H_vulgare -n 47 -t 17 -s 11354214 --prefix 10-hyde
```

[Josh, Figure out what is going on with run_hyde.py on your computer]

Note that in order to read the data, we needed to provide a little extra information. Specifically, we needed to provide the outgroup (H_vulgare), number of individuals sampled (47), number of species (17), and number of sites (11354214).

This command took like an hour to run.

We want to move the results to the `results` folder:
```
mv 10-hyde-out-filtered.txt ../results
mv 10-hyde-out.txt ../results
```

## Running HyDe on 10MB windows

Similarly to how we ran RAxML on each of the 10MB windows, we can use a bash script to run HyDe on each window. However, we first need to convert all the windows to the appropriate format.

In `code`, we open `python`:
```python
import os
from Bio import SeqIO

window_phylip_path = "../results/10concatenation10Mb_OneCopy-phylip/" 
os.makedirs(window_phylip_path,exist_ok=True)
window_path = "../data/Wheat_Relative_History_Data_Glemin_et_al/Concatenation10Mb_OneCopyGenes/"
all_windows = os.listdir(window_path)

for window in all_windows :
	records = SeqIO.parse(window_path+window, "fasta")
	count = SeqIO.write(records, window_phylip_path+window, "phylip-relaxed")
```

Note the above code did not work for me, so alternative code in 10-fasta2phylip.py run from the terminal: `python 10-fasta2phylip.py`.

In the paper, the authors run HyDe on all chromosomes, but that turns out to be too time-consuming, so we are only going to run on chromosom 3 (to reproduce Figure 3b).

I am going to create another folder `10concatenation10Mb_OneCopy-phylip-ch3` and I will move all files corresponding to this chromosome there:

In `results`:
```
mkdir 10concatenation10Mb_OneCopy-phylip-ch3
mv 10concatenation10Mb_OneCopy-phylip/*Chrom_3* 10concatenation10Mb_OneCopy-phylip-ch3
```

Now we can run HyDe on each window with the bash script `10-hyde-10mb.sh`:

In `code`:
```
./10-hyde-10mb.sh
```