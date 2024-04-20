# DESCRIPTION

This package aims to predict which neighborhoods in each UK city will gentrify over the next decade, and makes this information accessible using an intuitive and interactive map.

The package has the following file structure:

    ├───CODE
    │   ├───code
    │   ├───data
    │   │   ├───clean
    │   │   └───raw
    │   │       ├───api
    │   │       │   └───msoa
    │   │       │       └───counts
    │   │       │           ├───c2011
    │   │       │           └───c2021
    │   │       ├───geoportal
    │   │       ├───govuk
    │   │       └───ons
    │   └───viz
    └───DOC

For an overview of the project, including literature review, methodology, and conclusions, view the files in the DOC folder. The final visualization can be found in the CODE/viz folder.

If you would like to replicate our process and view the raw data, you can find all relevant files in the CODE folder.

# INSTALLATION

NOTE: This package uses Python.

In order to run all the code in this package, you will need to extract the CODE folder to your local files. Then we would recommend starting a virtual environment by running `python -m venv venv` in the terminal and running `pip install -r ELT_requirements.txt` to make sure you have all the necessary packages.

# EXECUTION

Run the files in this order:

1. dataEL.py
2. dataTPercentify.py
3. dataTCompile.py
4.