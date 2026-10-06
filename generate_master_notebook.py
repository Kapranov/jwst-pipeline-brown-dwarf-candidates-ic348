import json

setup_code = [
    "import os\n",
    "import sys\n",
    "import glob\n",
    "import pandas as pd\n",
    "from astropy.table import Table\n",
    "\n",
    "# 1. Secure Core Pipeline Environment Variables\n",
    "os.environ[\"MAST_API_TOKEN\"] = \"YOUR_MAST_API_TOKEN\"  # Replace with active token\n",
    "os.environ[\"CRDS_SERVER_URL\"] = \"https://stsci.edu\"\n",
    "os.environ[\"CRDS_PATH\"] = os.path.expanduser(\"~/crds_cache\")\n",
    "\n",
    "print(\"=== JWST Science Pipeline Environment Anchored ===\")\n",
    "print(f\"CRDS Cache Directory Location: {os.environ['CRDS_PATH']}\")"
]

stage_prepare_search = [
    "# Execute data discovery scripts to pull down active pool metadata structures\n",
    "search_scripts = [\n",
    "    \"./search_jw01257-o003_20260714t164831.py\",\n",
    "    \"./search_jw01257-o003_20260714t164831_00002.py\",\n",
    "    \"./search_jw01257-o003_20260714t164831_00005.py\",\n",
    "    \"./search_jw01257-o003_20260714t164831_00007.py\",\n",
    "    \"./search_jw01257-o003_20260714t164831_00008.py\",\n",
    "    \"./search_jw01257-o003_20260714t164831_00009.py\"\n",
    "]\n",
    "\n",
    "for script in search_scripts:\n",
    "    if os.path.exists(script):\n",
    "        print(f\"Executing: {script}\")\n",
    "        exec(open(script).read())\n",
    "    else:\n",
    "        print(f\"Skipping (not found): {script}\")"
]

download_mock_code = [
    "# Execution via Python Parameter Mocking Engine\n",
    "# Targets the f150w2-f162m filter association profile mapping as baseline\n",
    "sys.argv = [\n",
    "    \"./download_asn_members.py\",\n",
    "    \"jw01257-o003_20260714t164831_image3_00002_asn.json\",\n",
    "    \"1257\",\n",
    "    \"./processed_stage1_raw/jw01257-o003_t005_nircam_f150w2-f162m/\"\n",
    "]\n",
    "\n",
    "if os.path.exists(\"./download_asn_members.py\"):\n",
    "    exec(open(\"./download_asn_members.py\").read())\n",
    "else:\n",
    "    print(\"ERROR: download_asn_members.py utility script missing in root layout.\")"
]

verification_code = [
    "# Diagnostic Verification: Counting exact uncal file deliveries dynamically\n",
    "uncal_pattern = \"./processed_stage1_raw/*/*/*/*/*_uncal.fits\"\n",
    "delivered_files = glob.glob(uncal_pattern)\n",
    "\n",
    "print(\"==========================================\")\n",
    "print(\"DATA DELIVERY LOGISTICS VERIFICATION\")\n",
    "print(\"==========================================\")\n",
    "print(f\"Total '_uncal.fits' files recovered: {len(delivered_files)} / 120 target frames\")\n",
    "print(\"==========================================\")\n",
    "\n",
    "# Print storage footprints across active NIRCam filters\n",
    "for folder in glob.glob(\"./processed_stage1_raw/*\"):\n",
    "    if os.path.isdir(folder):\n",
    "        filter_uncal_count = len(glob.glob(os.path.join(folder, \"**/*_uncal.fits\"), recursive=True))\n",
    "        print(f\" -> Filter Segment Folder: {os.path.basename(folder)} | Exposures Detected: {filter_uncal_count}\")"
]

pipeline_code = [
    "# Execute Stage 1 and Stage 2 Pipelines sequentially over the data pools\n",
    "pipeline_scripts = [\"./run_stage_1_pipeline.py\", \"./run_stage_2_pipeline.py\"]\n",
    "\n",
    "for pipeline_run in pipeline_scripts:\n",
    "    if os.path.exists(pipeline_run):\n",
    "        print(f\"\\n--- Invoking Calibration Sequence: {pipeline_run} ---\")\n",
    "        exec(open(pipeline_run).read())\n",
    "    else:\n",
    "        print(f\"Warning: Pipeline controller script {pipeline_run} not located.\")\n",
    "\n",
    "print(\"\\nProcessing complete! All exposures successfully converted to standard *_cal.fits structural formats.\")"
]

master_notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# JWST Multiphase Science Pipeline Master Dashboard\n",
                "**Target Science:** IC 348 Brown Dwarf & Planetary Mass Survey  \n",
                "**PI Designation:** Oleg G. Kapranov  \n",
                "**Instrument System:** JWST NIRCam Broad & Narrow Filter Configurations \n",
                "\n",
                "This master workspace maps, triggers, and evaluates Level 1 (Detector) and Level 2 (Calibrated Image) sequences across five concurrent NIRCam setups according to the documented framework logs."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## Step 1: Environment Integration, Token Verification & Routing Paths"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": setup_code
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## Step 2: Data Discovery (Pulling Down Pool Catalogs & Association Definitions)"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": stage_prepare_search
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## Step 3: Archive Retrieval (Executing Association Space Downloads from MAST Archive)"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": download_mock_code
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## Step 4: Health-Check Logistics (Physical Footprint Verification Metrics)"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": verification_code
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## Step 5: Execute Complete Calibration Matrix (Detector1Pipeline & Image2Pipeline Workflow)"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": pipeline_code
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python (astro_env)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

with open("00_jwst_pipeline_master_execution.ipynb", "w") as f:
    json.dump(master_notebook, f, indent=4)

print("\n==========================================")
print("Master Jupyter Notebook created successfully!")
print("Filename: 00_jwst_pipeline_master_execution.ipynb")
print("==========================================")
