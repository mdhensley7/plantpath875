---
layout: default
title: 03 Data and Softwate Setup
parent: S26 Wheat
nav_order: 2
---

# Cloning the class repository

Most class materials are accessible from the [course repository](https://github.com/solislemuslab/phylo-practicum/tree/main). If you have [git](https://git-scm.com/) downloaded, you can clone this repo with the command `git clone https://github.com/solislemuslab/phylo-practicum`. 

Specifically, there is a folder called `glemin-wheat` that we will be using for this course. This folder contains all scripts necessary to recreate the analyses of [Glemin et al (2019)](https://www.science.org/doi/10.1126/sciadv.aav9188). These scripts assume the specific directory structure that is already set up in this repo. While we encourage students to use this structure, you can organize your files however makes the most sense for you, but be noted that some scripts may need to be altered accordingly. The structure we use is:
```
glemin-wheat/
├── index.md            <-- Contains an Overview of the contents
├── data/
│   ├── Wheat_Relative_History_Data_Glemin_et_al/   Folder that will contain the wheat data.
│   │	├── README.txt     <-- Describes the downloadable data from the paper
├── code/                  <-- Scripts and bash files to run the analyses.
│ ├── Y-XXXXX.md     <-- Markdown for class number Y on how to run XXXXX analyses
| ├── Y-ZZZZZ.sh     <-- Bash script for class number Y to run analysis ZZZZZ
├── results/               <-- This folder will contain the results generated for each analysis

```

# Downloading the data

The authors of the paper made data publicly available in a clean manner in this [data repository](https://www.agap-ge2pop.org/wheat-relative-history/).

We will download the [Wheat_Relative_History_Data_Glemin_et_al.zip](https://www.agap-ge2pop.org/wp-content/uploads/WheatRelativeHistory/download/Wheat_Relative_History_Data_Glemin_et_al.zip) and move it into our `data` subfolder.

We will need to extract the folder itself from the zipped file. After unzipping, the folder will contain more data folders that are zipped. You will additionally need to extract the contents of `IndividualAlignements_OneCopyGenes.zip` file. At the end your directory structure should look like this:

```
glemin-wheat/

├── data/
│   ├── Wheat_Relative_History_Data_Glemin_et_al/
│	|	├── OneCopyGenes
│	│   │	├── T_urartu_Tr309_URA15_Singlet902_simExt_macseNT_noFS_clean.aln
│	│   │	├── T_urartu_Tr309_URA15_Singlet9090_simExt_macseNT_noFS_clean.aln
│	│   │	├── ...
```

The authors uploaded the alignments, rather than raw data for us to assemble and align. 


# Installing required software

## Software Note on Windows

For Windows users, some software is only available on Linux/Mac or has different installation instructions for Windows users. Fortunately Windows 11 (and more recent versions of Windows 10) can create a Linux-like environment relatively easily using the [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/about). Detailed installation instructions can be found [here](https://learn.microsoft.com/en-us/windows/wsl/install) or from the command line you can run:
```
wsl --install
```

Now, from the command prompt you can enter `wsl` and you should enter a Linux environment where you can effectively install and use software that requires a Linux operating system. From here you _should_ be able to use any software that only has a Linux/Mac installation instructions. It is important to note that like with any operating system, the programs need to be accessible from the command line. An easy way to do this is to ensure your software is located somewhere in your `PATH`. You can check the folders that are a part of your path with `echo $PATH`.


## 1. RAxML Next Generation

The repository for RAxML has installation instructions [here](https://github.com/amkozlov/raxml-ng).

### For Mac

I click on `Download OSX/macOS binary (x86 and ARM)` and I download `raxml-ng_v1.2.2_macos.zip`. I put this folder in my computer (I have a folder `software`), and inside it is the executable `raxml-ng`.

I will copy this executable into `/usr/local/bin` so that I can call it from wherever in my machine, but you can also use the whole path.

```
cd software/raxml-ng_v1.2.2_macos/ ## you need to modify to your own path
ls ## check the raxml-ng executable is there
cp raxml-ng /usr/local/bin
```

When you try to run `raxml-ng`, your computer will complain that it cannot verify it is free of malware. You need to go to System Settings > Privacy and Security. Find the app and choose "Open Anyway". 
Note that if you copied your executable on your PATH, you will need to choose "open anyway" twice: once for the file in the original path and once for when you call it somewhere else in your machine.

Confirm that you can run RAxML by typing `raxml-ng` in the terminal.


### For Windows 

This will need to be built in the Windows Subsystem for Linux. First, download the Linux binary for [RAxML-ng](https://github.com/amkozlov/raxml-ng/releases/download/1.2.2/raxml-ng_v1.2.2_linux_x86_64.zip). Extract the contents from this folder and you will find an executable file named `raxml-ng`, either add the location of raxml-ng to your `PATH` or move the file to a location already in your `PATH`. Now from the WSL, you can confirm you have installed RAxML with the command `raxml-ng -h`.


## 2. SuperTriplets

SuperTriplets comes packaged as a Java program and thus requires Java. You can check if you have Java installed on your machine with the command `java -h`. If Java is not installed, you can download it [here](https://www.java.com/en/). 

**Note for Windows users**: unless you explicitly download Java in the WSL, you will only be able to use Java programs outside your WSL (i.e., in the normal command prompt before typing `wsl`).

There is download information in the SuperTriplets [website](https://www.agap-ge2pop.org/supertriplets/download/).

You simply download the java file `SuperTriplets_v1.1.jar`. I put it in my computer `software` folder inside a subfolder named `supertriplets`. We will have to use the whole path when calling this function:
```
java -jar -Xmx500m ~/software/supertriplets/SuperTriplets_v1.1.jar newick_file.nwk outfile
```

## 3. ASTRAL

The [ASTRAL repo](https://github.com/smirarab/ASTRAL) recommends us to use the new C code [ASTER](https://github.com/chaoszhang/ASTER). Installation instructions are within.


### For Mac

For me, installing with conda worked:
```
conda config --add channels bioconda
conda install aster
```

To know where everything was installed:
```
$ which wastral
/Users/Clauberry/.julia/conda/3/bin/wastral
```

And you can test it works by:
```
$ wastral
```


### For Windows 

You can download the binary from [here](https://github.com/chaoszhang/ASTER/archive/refs/heads/Windows.zip). All of the various forms of ASTRAL are included in the `exe/` folder and you should make sure these files are a part of your `PATH`. You can confirm correct installation by running `waster -h`.

Alternatively, if you need to install from source, you can build in WSL and installation instructions can be found [here](https://github.com/chaoszhang/ASTER?tab=readme-ov-file#for-linuxmacoswsl-users).

## 4. Julia and packages

I recommend installing Julia via [JuliaUp](https://github.com/JuliaLang/juliaup) as this allows you to have multiple Julia versions installed. 

### For Mac

Install JuliaUp:
```
curl -fsSL https://install.julialang.org | sh
```

Install Julia (you may need to restart your terminal before you can run this command):
```
juliaup add release
```

### For Windows

Julia can be installed by following the directions [here](https://julialang.org/downloads/) or directly from the Julia website [Windows app store](https://apps.microsoft.com/detail/9njnww8pvkmn?hl=en-US&gl=US).

### Once Julia is Installed


Start Julia by typing `julia` in the terminal.
Inside Julia, install packages by first pressing `]` to go into package mode (the prompt will change to `(@v1.12) pkg>`):
```
add PhyloNetworks
add SNaQ
add PhyloPlots
add CSV
add DataFrames
```
Leave Julia by typing `exit()`.

## 5. HyDe

We will follow the installation commands from the [github repo](https://github.com/pblischak/HyDe).

HyDe requires Python. You can install the latest version of Python for your machine [here](https://www.python.org/downloads/). You can check installation by running the command `python -h` or `pythonX.XX -h` where X.XX is the version number of python.


The files can be downloaded with:
```
git clone https://github.com/pblischak/HyDe.git
```

Next move into the HyDe folder and install HyDe:
```
cd HyDe
python3 -m pip install -r requirements.txt
python3 -m pip install .
```

**Note for Mac users** that I had updated XCode, but did not agree to the new license, so I was getting weird errors because of that.

**Note for Windows users:** I recommend downloading Python and installing HyDe from the WSL. HyDe can be built natively in Windows but requires Visual C++ which is bulky (see below). Most WSL distributions come with Python already installed, you can confirm this by typing `python3 --version`. You will additionally need `pipx` to globally install HyDe:
```
sudo apt install pipx
```

From here you can install Hyde from PyPI with the command:
``` 
pipx install phyde
```

Alternatively, to install natively on Windows (not recommended), you will need 
a the Microsoft Visual C++ compiler that is at least version 14.0; that can be downloaded [here]( https://visualstudio.microsoft.com/visual-cpp-build-tools/
). When going thru the installer, select "Desktop Development with C++".

You can confirm installation by running `run_hyde.py`.

## 6. R

Those that don't have them should install R and RStudio, see [here](https://posit.co/download/rstudio-desktop/).

Inside R:
```
install.packages("ape")
install.packages("phangorn")
install.packages("BiocManager")
BiocManager::install("remotes")
BiocManager::install("YuLab-SMU/treedataverse")
install.packages("MSCquartets")
install.packages("phytools")
install.packages("ggplot2")
```


# Unused software

The authors used the following software that we won't use:

## bppSuite

The software repository has instructions for installation [here](https://github.com/BioPP/bppsuite).

Before git cloning `bppsuite`, we need to make sure we have installed specific libraries.

### For Mac

Following [this](https://github.com/BioPP/bpp-documentation/wiki/Installation), we do:

```
brew tap jydu/homebrew-biopp
brew update ## optional
brew install libbpp-core libbpp-seq libbpp-phyl libbpp-popgen
```
Note that I had to update my OS and XCode.

Note that the libraries names change per Homebrew notation.

These are the project or library names:
- `bpp-core`
- `bpp-seq`
- `bpp-phyl`
- `bpp-popgen`


Homebrew prefixes most C/C++ libraries with lib to make it explicit that they install libraries, hence:
- `libbpp-core`
- `libbpp-seq`
- `libbpp-phyl`
- `libbpp-popgen`

I get the following error due to `cmake` version:

```
$ brew install libbpp-core libbpp-seq libbpp-phyl libbpp-popgen
==> Fetching downloads for: libbpp-core, libbpp-seq, libbpp-phyl and libbpp-popgen
✔︎ Bottle Manifest cmake (4.2.1)                           [Downloaded   11.4KB/ 11.4KB]
✔︎ Bottle cmake (4.2.1)                                    [Downloaded   20.1MB/ 20.1MB]
✔︎ Formula libbpp-core (2.4.1)                             [Verified    361.3KB/361.3KB]
✔︎ Formula libbpp-seq (2.4.1)                              [Verified    322.6KB/322.6KB]
✔︎ Formula libbpp-phyl (2.4.1)                             [Verified    600.4KB/600.4KB]
✔︎ Formula libbpp-popgen (2.4.1)                           [Verified    116.9KB/116.9KB]
==> Installing libbpp-core from jydu/biopp
==> Installing jydu/biopp/libbpp-core dependency: cmake
==> Pouring cmake--4.2.1.sequoia.bottle.tar.gz
🍺  /usr/local/Cellar/cmake/4.2.1: 4,016 files, 66.8MB
==> cmake ..
Last 15 lines from /Users/Clauberry/Library/Logs/Homebrew/libbpp-core/01.cmake.log:
-Wno-dev
-DBUILD_TESTING=OFF
-DCMAKE_OSX_SYSROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX15.sdk

CMake Error at CMakeLists.txt:8 (cmake_minimum_required):
  Compatibility with CMake < 3.5 has been removed from CMake.

  Update the VERSION argument <min> value.  Or, use the <min>...<max> syntax
  to tell CMake that the project requires at least <min> but has been updated
  to work with policies introduced by <max> or earlier.

  Or, add -DCMAKE_POLICY_VERSION_MINIMUM=3.5 to try configuring anyway.


-- Configuring incomplete, errors occurred!

If reporting this issue please do so at (not Homebrew/* repositories):
  https://github.com/jydu/homebrew-biopp/issues
```

I asked ChatGPT, and they suggest forcing the cmake version:

```
export CMAKE_POLICY_VERSION_MINIMUM=3.5
brew install libbpp-core
```
or
```
brew install libbpp-core \
  --cmake-args="-DCMAKE_POLICY_VERSION_MINIMUM=3.5"
```
But neither works!

From the paper, it seems they only use `bppSuite` for re-rooting the gene trees:
"BppReroot of the BppSuite (42, 43) was used to reroot the 13,288 gene trees, using as outgroups the following ordered list of species: H_vulgare, Er_bonaepartis, S_vavilovii, and Ta_caputMedusae."

So, we will skip this software for now.

## SSIMUL

We download the binaries from the software website for Mac and Linux [here](http://www.atgc-montpellier.fr/ssimul/).

The zipped folder `ssimul.zip` contains the executables.

**Note for Windows users:** We will use again the Windows Subsystem for Linux.