import json
import os

notebook_path = "00_jwst_pipeline_master_execution.ipynb"

# Structuring a publication-grade HTML warning box styled with a red boundary fill
attention_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "<div style='padding: 15px; border: 2px solid #D9534F; border-radius: 5px; background-color: #FDF2F2; color: #B94A48;'>\n",
        "    <h3 style='margin-top: 0; color: #D9534F; font-weight: bold;'>⚠️ STAGE 5: CRITICAL STORAGE & DISK SPACE WARNING</h3>\n",
        "    <p style='font-size: 13px; line-height: 1.5;'>\n",
        "        <strong>ATTENTION OPERATOR:</strong> JWST raw exposure calibrations require massive array allocations. To prevent local system drive saturation, <strong>DO NOT</strong> dump large batches of files into the ingestion path simultaneously.\n",
        "    </p>\n",
        "    <p style='font-size: 13px; line-height: 1.5;'>\n",
        "        Process exposures sequentially by dropping <strong>ONLY ONE raw file at a time</strong> into the target directory path:<br>\n",
        "        <code>./processed_stage1_raw/jw01257-o003_t005_nircam_f150w2-f164n/</code>\n",
        "    </p>\n",
        "    <p style='font-size: 13px; line-height: 1.5; margin-bottom: 0;'>\n",
        "        Failure to partition inputs will expand the local cache directory footprint beyond system limits (<strong>~50 to 100 GB allocation spike</strong>), resulting in a hard kernel panic crash.\n",
        "    </p>\n",
        "</div>"
    ]
}

if os.path.exists(notebook_path):
    with open(notebook_path, "r") as f:
        nb = json.load(f)

    # Append the red markdown warning cell to the notebook
    nb["cells"].append(attention_cell)

    with open(notebook_path, "w") as f:
        json.dump(nb, f, indent=4)

    print("\n==========================================")
    print("Stage 5 Red Attention Box successfully injected!")
    print("==========================================")
else:
    # Fallback configuration: If the notebook doesn't exist yet, create a fresh one with this cell
    fresh_notebook = {
        "cells": [attention_cell],
        "metadata": {"kernelspec": {"display_name": "Python 3", "name": "python3"}, "language_info": {"name": "python"}},
        "nbformat": 4, "nbformat_minor": 2
    }
    with open(notebook_path, "w") as f:
        json.dump(fresh_notebook, f, indent=4)
    print("\n==========================================")
    print("Master notebook initialized with Stage 5 Red Attention Alert!")
    print("==========================================")
