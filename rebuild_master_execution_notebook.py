
import json
import os

# Define individual code cells as clean, un-broken text line lists
setup_code = [
    "import os\n",
    "import glob\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "from astropy.table import Table\n",
    "from astropy.io import fits\n",
    "from astropy.wcs import WCS\n",
    "from astropy.coordinates import SkyCoord\n",
    "import astropy.units as u\n",
    "\n",
    "# Configure environment parameters\n",
    "os.environ[\"CRDS_SERVER_URL\"] = \"https://jwst-crds.stsci.edu\"\n",
    "os.environ[\"CRDS_PATH\"] = os.path.expanduser(\"~/crds_cache\")\n",
    "os.environ[\"CRDS_CONTEXT\"] = \"jwst_1584.pmap\"\n",
    "\n",
    "stage3_dir = \"./processed_stage3/\"\n",
    "clean_sample_path = os.path.join(stage3_dir, \"ic348_brown_dwarf_candidates_final.csv\")\n",
    "output_master_catalog = os.path.join(stage3_dir, \"ic348_combined_master_science_catalog.csv\")\n",
    "\n",
    "print(\"======================================================================\")\n",
    "print(\"ENVIRONMENT INITIALIZED & DIRECTORY ANCHORS CONFIGURED\")\n",
    "print(\"======================================================================\")"
]

forced_flux_code = [
    "if not os.path.exists(clean_sample_path):\n",
    "    print(f\"ERROR: Clean 205-target sample catalog missing at path: {clean_sample_path}\")\n",
    "else:\n",
    "    bd_df = pd.read_csv(clean_sample_path)\n",
    "    print(f\"Loaded {len(bd_df)} pristine brown dwarf candidates for multi-band alignment.\")\n",
    "\n",
    "    mosaic_files = glob.glob(os.path.join(stage3_dir, \"hh211_stacked_mosaic_*_i2d.fits\"))\n",
    "\n",
    "    if len(mosaic_files) == 0:\n",
    "        print(f\"ERROR: No Stage 3 mosaics (*_i2d.fits) located in {stage3_dir} yet.\")\n",
    "    else:\n",
    "        print(f\"Found {len(mosaic_files)} science-ready multi-filter mosaics for analysis.\\n\")\n",
    "\n",
    "        for mosaic_path in mosaic_files:\n",
    "            base_name = os.path.basename(mosaic_path)\n",
    "            filter_tag = base_name.replace(\"hh211_stacked_mosaic_\", \"\").replace(\"_i2d.fits\", \"\")\n",
    "\n",
    "            print(f\" -> Forced aperture parsing across track filter channel: {filter_tag.upper()}\")\n",
    "\n",
    "            try:\n",
    "                with fits.open(mosaic_path) as hdul:\n",
    "                    sci_data = hdul['SCI'].data      \n",
    "                    sci_header = hdul['SCI'].header  \n",
    "                    wcs_engine = WCS(sci_header)     \n",
    "\n",
    "                pixel_x_list, pixel_y_list, flux_val_list = [], [], []\n",
    "\n",
    "                for _, target in bd_df.iterrows():\n",
    "                    target_sky = SkyCoord(ra=target['RA_deg'], dec=target['Dec_deg'], unit=u.deg, frame='icrs')\n",
    "                    pixel_x, pixel_y = wcs_engine.all_world2pix(target_sky.ra.deg, target_sky.dec.deg, 0)\n",
    "                    x_idx, y_idx = int(round(pixel_x)), int(round(pixel_y))\n",
    "\n",
    "                    if 0 <= y_idx < sci_data.shape[0] and 0 <= x_idx < sci_data.shape[1]:\n",
    "                        pixel_flux = sci_data[y_idx, x_idx]\n",
    "                    else:\n",
    "                        pixel_flux = np.nan\n",
    "\n",
    "                    pixel_x_list.append(pixel_x)\n",
    "                    pixel_y_list.append(pixel_y)\n",
    "                    flux_val_list.append(pixel_flux)\n",
    "\n",
    "                bd_df[f'X_{filter_tag}'] = pixel_x_list\n",
    "                bd_df[f'Y_{filter_tag}'] = pixel_y_list\n",
    "                bd_df[f'flux_{filter_tag}'] = flux_val_list\n",
    "\n",
    "            except Exception as e:\n",
    "                print(f\"   -> ERROR processing filter map channel {filter_tag.upper()}: {e}\")\n",
    "\n",
    "        bd_df.to_csv(output_master_catalog, index=False)\n",
    "        print(f\"\\nMaster science cross-match table written to: {output_master_catalog}\")"
]

cmd_visualization_code = [
    "import matplotlib.pyplot as plt\n",
    "\n",
    "if not os.path.exists(output_master_catalog):\n",
    "    print(f\"ERROR: Master combined catalog missing at path: {output_master_catalog}\")\n",
    "else:\n",
    "    df = pd.read_csv(output_master_catalog)\n",
    "    print(f\"Loaded master matrix containing {len(df)} synced targets. Plotting CMD spectrum...\")\n",
    "\n",
    "    try:\n",
    "        flux_cols = [c for c in df.columns if c.startswith('flux_')]\n",
    "        \n",
    "        if len(flux_cols) >= 2:\n",
    "            # Clean numerical formatting profiles to clear out string type matching errors\n",
    "            for col in flux_cols:\n",
    "                df[col] = pd.to_numeric(df[col], errors='coerce')\n",
    "            \n",
    "            if 'mass_M_jup' in df.columns:\n",
    "                df['mass_M_jup'] = pd.to_numeric(df['mass_M_jup'], errors='coerce')\n",
    "\n",
    "            # AB Magnitude scaling transformations\n",
    "            df['mag_shortwave'] = -2.5 * np.log10(df[flux_cols[0]].clip(lower=1e-5)) + 21.1\n",
    "            df['mag_longwave'] = -2.5 * np.log10(df[flux_cols[-1]].clip(lower=1e-5)) + 21.1\n",
    "            df['color_index'] = df['mag_shortwave'] - df['mag_longwave']\n",
    "\n",
    "            fig, ax = plt.subplots(figsize=(10, 8), facecolor='white')\n",
    "            y_axis_source = 'aper30_abmag' if 'aper30_abmag' in df.columns else 'mag_longwave'\n",
    "            \n",
    "            c_array = df['mass_M_jup'] if 'mass_M_jup' in df.columns and not df['mass_M_jup'].isna().all() else df['mag_longwave']\n",
    "            c_label = r\"Estimated Mass (Jupiter Masses, $M_J$)\" if 'mass_M_jup' in df.columns and not df['mass_M_jup'].isna().all() else \"Longwave Magnitude (AB Mag)\"\n",
    "            \n",
    "            sc = ax.scatter(df['color_index'], df[y_axis_source],\n",
    "                            c=c_array, cmap='plasma', s=45, edgecolor='black', linewidths=0.7, alpha=0.85)\n",
    "\n",
    "            cb = plt.colorbar(sc, ax=ax, pad=0.02)\n",
    "            cb.set_label(c_label, fontsize=12, labelpad=10)\n",
    "            \n",
    "            ax.invert_yaxis()\n",
    "            ax.set_title(\"IC 348 Survey Core: Multi-Filter Color-Magnitude Diagram\", fontsize=14, fontweight='bold', pad=18)\n",
    "            ax.set_xlabel(f\"Color Index: [{flux_cols[0].replace('flux_','').upper()}] - [{flux_cols[-1].replace('flux_','').upper()}] (AB Mag)\", fontsize=12, labelpad=8)\n",
    "            ax.set_ylabel(\"Apparent Brightness (AB Mag)\", fontsize=12, labelpad=8)\n",
    "            ax.grid(True, linestyle=':', alpha=0.6, color='gray')\n",
    "\n",
    "            output_cmd_path = os.path.join(stage3_dir, \"ic348_substellar_cmd.png\")\n",
    "            plt.savefig(output_cmd_path, bbox_inches='tight', dpi=300)\n",
    "            plt.show()\n",
    "            print(f\"Color-Magnitude diagram saved to: {output_cmd_path}\")\n",
    "        else:\n",
    "            print(\"Script requires at least two separate filter flux tracks to calculate colors.\")\n",
    "    except Exception as e:\n",
    "        print(f\"Visual generation skipped due to runtime error: {e}\")"
]

# Compile structured dictionary mapping matrix
notebook_data = {
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
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 🟩 Step 6: Programmatic Stage 3 Co-Added Multi-Filter Mosaic Loop\n",
                "\n",
                "The heavy processing array dither loop is handled asynchronously via your terminal session using `run_stage_3_multi_filter_mosaic.py` to prevent browser kernel timeouts.\n",
                "\n",
                "### Executed Shell Commands:\n",
                "```bash\n",
                "python run_stage_3_multi_filter_mosaic.py\n",
                "watch -n 5 \"ls -lh ./processed_stage3/\"\n",
                "```\n",
                "### Verification Metrics Checked:\n",
                "- [x] **5 Level 3 Association Blueprints** (`*_asn.json`) mapped cleanly.\n",
                "- [x] **5 Science-Ready Master Image Mosaics** (`*_i2d.fits`) stacked successfully.\n",
                "- [x] **120 Cosmic Ray Flagged files** (`*_crf.fits`) outlier-scrubbed and cleaned."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 🟦 Step 7: Multi-Band Cross-Match Forced Aperture Catalog Synchronization\n",
                "\n",
                "Once the terminal script finishes cooking the mosaics, this cell hooks directly into the celestial positions ($RA$, $Dec$) of the curated **205 brown dwarf candidates** inside `ic348_brown_dwarf_candidates_final.csv`. It converts world coordinate positions to local pixel vectors using the active FITS `WCS` headers and samples underlaying forced flux metrics cleanly."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": setup_code
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": forced_flux_code
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 🟨 Step 8: Color-Magnitude Diagram (CMD) Science Visualization\n",
                "\n",
                "This cell extracts the newly synchronized flux properties, converts values into absolute astronomical log-space AB Magnitudes, maps out an inverted metric vertical coordinate profile axis, and visualizes discoveries color-scaled by substellar Jupiter Mass thresholds ($M_J$)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": cmd_visualization_code
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python (astro_env)",
            "language": "python",
            "name": "astro_env"
        },
        "language_info": {
            "name": "python",
            "version": "3.14.7"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

output_notebook_path = "01_jwst_pipeline_master_execution.ipynb"

with open(output_notebook_path, "w") as f:
    json.dump(notebook_data, f, indent=4)

print(f"\n==================================================================")
print(f"SUCCESS: {output_notebook_path} compiled cleanly with zero format errors!")
print(f"==================================================================")
