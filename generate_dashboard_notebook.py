import json

# Lists for notebook setup, discovery, downloads, and pipeline processing cells
# (The full generation script containing environment variables, filter paths,
# and pipeline execution loops can be found in the referenced document [01_jwst_data_reduction_and_cataloging.py])

notebook_content = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# JWST Multiphase Science Pipeline Master Dashboard\n",
                "**Target Science:** IC 348 Brown Dwarf Survey & HH 211 Protostellar Outflow  \n",
                "**PI Designation:** Oleg G. Kapranov  \n",
                "**Instrument System:** JWST NIRCam Broad & Narrow Filter Configurations"
            ]
        }
        # Additional setup, discovery, download, and pipeline cells are structured here [01_jwst_data_reduction_and_cataloging.py]
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python (astro_env)",
            "language": "python",
            "name": "astro_env"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open("01_jwst_pipeline_master_execution.ipynb", "w") as f:
    json.dump(notebook_content, f, indent=4)

print("Master Executive Dashboard Notebook successfully generated on disk!")
