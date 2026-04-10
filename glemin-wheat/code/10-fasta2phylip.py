from pathlib import Path
from Bio import SeqIO

# input and output directories
in_dir = Path("../data/Wheat_Relative_History_Data_Glemin_et_al/Concatenation10Mb_OneCopyGenes")
out_dir = Path("../results/10concatenation10Mb_OneCopy-phylip")
out_dir.mkdir(parents=True, exist_ok=True)

# loop over FASTA files
for fasta_file in in_dir.glob("*.fasta"):
    # output file name: same stem, new extension
    phylip_file = out_dir / (fasta_file.stem + ".phy")

    records = list(SeqIO.parse(fasta_file, "fasta"))

    if len(records) == 0:
        print(f"Skipping {fasta_file.name}: no sequences found")
        continue

    SeqIO.write(records, phylip_file, "phylip-relaxed")
    print(f"Converted {fasta_file.name} → {phylip_file.name}")