# Components - Instructions

Before running any components, install anaconda/miniconda on your computer

Download [miniconda3](https://docs.conda.io/en/latest/miniconda.html)

# Instantiating Conda Environment
## Windows

After installing, Instantiate anaconda/miniconda3 by opening from search bar


## Linux
Run the following commands in the terminals:

    mkdir -p ~/miniconda3
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
    rm -rf ~/miniconda3/miniconda.sh
    ~/miniconda3/bin/conda init bash
    ~/miniconda3/bin/conda init zsh

It should appear like the following:


    (base) some_directory:

If it does not then try:

    source miniconda3/bin/activate

# Installing environment

Navigate to the project folder:

`cd data-engineeering-pipeline`

You can create a virtual environment from the following code for this project:
    
    `conda env create -f environment.yaml`

# Activating Environment

You need to activate environment before running any particular component

After environment creation, the following code will help you activate environment:

    conda activate data_pipeline

# Running Components

Navigate to each components' folder to find instructions for running pipeline/ separate component.