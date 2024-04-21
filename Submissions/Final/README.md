# DESCRIPTION

This package aims to predict which neighborhoods in each UK city will gentrify over the next decade, and make this information accessible using an intuitive and interactive map.

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

In order to run all the code in this package, you will need to extract the CODE folder to your local files. Then we would recommend starting a virtual environment and running `pip install -r ELT_requirements.txt modeling_and_analysis_ipynb_requirements.txt` to make sure you have all the necessary libraries.

If you would like to view the final visualization, please [download](https://powerbi.microsoft.com/en-us/downloads/) and install Microsoft Power BI Desktop. The free version is good enough.

# EXECUTION

1. Data (Run the files in this order. Income and pricing data have been included in the package, but census data will have to be downloaded because the file size is too big to be included here)
    - dataEL.py
    - dataTPercentify.py
    - dataTCompile.py
2. Modeling (Run the cells in each notebook sequentially. The required CSVs are in "modeling_data" folder)
    - Manchester LSOA Modeling.ipynb
    - UK Gentrification NN.ipynb
    - UK Gentrification RF_XGB_SHAP.ipynb
    - Post Modeling Gentrification Analysis.ipynb
3. Visualization (Open the following file in Power BI)
    - Gentrification Analysis.pbix
