#!/bin/bash

DATADIR="../results/10concatenation10Mb_OneCopy-phylip-ch3"
mkdir ../results/HyDe/
mkdir ../results/HyDe/10Mb-concatenation-ch3

for file in "$DATADIR"/*; do
	echo "Processing file: $file"
    
    # 1. Extract the filename from the path
    filename=$(basename "$file")
    
    # 2. Remove the extension
    base="${filename%.*}"

    run_hyde.py -i "$file" -m ../results/07-species_mapping.txt -o H_vulgare -n 47 -t 17 -s 11354214 --prefix "../results/HyDe/10Mb-concatenation-ch3/$base"
done