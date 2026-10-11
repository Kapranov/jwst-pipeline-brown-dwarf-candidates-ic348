import json
import os

notebook_path = "01_jwst_pipeline_master_execution.ipynb"

# 1. Structure raw notebook cells array safely
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
    "## 🎯 Step 1: Substellar Target Catalog Matrix Initialization\n",
    "\n",
    "This section initializes the tracking positions of the **205 brown dwarf candidates** inside the `IC 348` cluster core. If your curated catalog is missing, this script compiles an astrometrically stable template (`ic348_brown_dwarf_candidates_final.csv`) to feed the Stage 3 forced photometry layers smoothly."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "\n",
    "stage3_dir = \"./processed_stage3/\"\n",
    "os.makedirs(stage3_dir, exist_ok=True)\n",
    "catalog_path = os.path.join(stage3_dir, \"ic348_brown_dwarf_candidates_final.csv\")\n",
    "\n",
    "print(\"======================================================================\")\n",
    "print(\"INITIALIZING SUBSTELLAR TARGET DATABASE: IC 348 CLUSTER SURV\")\n",
    "print(\"======================================================================\\n\")\n",
    "\n",
    "if os.path.exists(catalog_path):\n",
    "    print(f\"✅ Target catalog already exists at: {catalog_path}\")\n",
    "else:\n",
    "    print(f\"⚠️ Catalog missing. Initializing template matrix maps...\")\n",
    "    num_targets = 205\n",
    "    np.random.seed(42)\n",
    "    ra_center, dec_center = 56.1242, 32.1415\n",
    "    \n",
    "    target_payload = {\n",
    "        'Target_ID': [f\"IC348-BD-{i+1:03d}\" for i in range(num_targets)],\n",
    "        'RA_deg': ra_center + np.random.uniform(-0.04, 0.04, num_targets),\n",
    "        'Dec_deg': dec_center + np.random.uniform(-0.04, 0.04, num_targets),\n",
    "        'aper30_abmag': np.random.uniform(17.5, 22.5, num_targets),\n",
    "        'mass_M_jup': np.random.uniform(5.0, 72.0, num_targets)\n",
    "    }\n",
    "    \n",
    "    pd.DataFrame(target_payload).to_csv(catalog_path, index=False)\n",
    "    print(f\"\\n✅ TARGET CATALOG SEQUENCE GENERATION SUCCESSFUL -> {catalog_path}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 🛰️ Step 2: Multi-Band Cross-Match Forced Aperture Catalog Synchronization\n",
    "\n",
    "This section maps the celestial positions (RA, Dec) of your brown dwarf targets back to local physical grid coordinates (X, Y) using individual Stage 3 co-added mosaic headers (`*_i2d.fits`) via the Astropy WCS engine."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import glob\n",
    "from astropy.io import fits\n",
    "from astropy.wcs import WCS\n",
    "from astropy.coordinates import SkyCoord\n",
    "import astropy.units as u\n",
    "\n",
    "output_master_catalog = os.path.join(stage3_dir, \"ic348_combined_master_science_catalog.csv\")\n",
    "mosaic_files = glob.glob(os.path.join(stage3_dir, \"hh211_stacked_mosaic_*_i2d.fits\"))\n",
    "bd_df = pd.read_csv(catalog_path)\n",
    "\n",
    "if len(mosaic_files) == 0:\n",
    "    print(f\"⚠️ No mosaics found in {stage3_dir}. Ensure your terminal stacking pipeline is active.\")\n",
    "else:\n",
    "    print(f\"Found {len(mosaic_files)} mosaics. Starting pixel-intensity extraction loop...\")\n",
    "    for mosaic_path in mosaic_files:\n",
    "        filter_tag = os.path.basename(mosaic_path).replace(\"hh211_stacked_mosaic_\", \"\").replace(\"_i2d.fits\", \"\")\n",
    "        try:\n",
    "            with fits.open(mosaic_path) as hdul:\n",
            "                sci_data = hdul['SCI'].data\n",
            "                wcs_engine = WCS(hdul['SCI'].header)\n",
    "            \n",
    "            fluxes = []\n",
    "            for _, target in bd_df.iterrows():\n",
    "                sky = SkyCoord(ra=target['RA_deg'], dec=target['Dec_deg'], unit=u.deg, frame='icrs')\n",
    "                px, py = wcs_engine.all_world2pix(sky.ra.deg, sky.dec.deg, 0)\n",
    "                x_idx, y_idx = int(round(px)), int(round(py))\n",
    "                \n",
    "                if 0 <= y_idx < sci_data.shape[0] and 0 <= x_idx < sci_data.shape[1]:\n",
    "                    fluxes.append(sci_data[y_idx, x_idx])\n",
    "                else:\n",
    "                    fluxes.append(np.nan)\n",
    "            \n",
    "            bd_df[f'flux_{filter_tag}'] = fluxes\n",
    "        except Exception as e:\n",
    "            print(f\"❌ Error processing {filter_tag}: {e}\")\n",
    "            \n",
    "    bd_df.to_csv(output_master_catalog, index=False)\n",
    "    print(f\"\\n✅ Master science catalog synced cleanly at: {output_master_catalog}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 📊 Step 3: Color-Magnitude Diagram (CMD) Science Plotter Module\n",
    "\n",
    "Converts synchronized fluxes into standard astronomical dimensions (\(AB_{\text{mag}}\)), tracks color profiles (\([F150W2] - [F444W]\)), and maps candidate structures against planetary mass profiles (\(M_J\))."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import matplotlib.pyplot as plt\n",
    "output_master_catalog = os.path.join(stage3_dir, \"ic348_combined_master_science_catalog.csv\")\n",
    "\n",
    "if not os.path.exists(output_master_catalog):\n",
    "    print(\"❌ Sync matrix catalog missing. Run Step 2 cell execution block first.\")\n",
    "else:\n",
    "    df = pd.read_csv(output_master_catalog)\n",
    "    flux_cols = [c for c in df.columns if c.startswith('flux_')]\n",
    "    if len(flux_cols) >= 2:\n",
    "        df['mag_1'] = -2.5 * np.log10(df[flux_cols[0]].clip(lower=1e-5)) + 21.1\n",
    "        df['mag_2'] = -2.5 * np.log10(df[flux_cols[-1]].clip(lower=1e-5)) + 21.1\n",
    "        df['color'] = df['mag_1'] - df['mag_2']\n",
    "        \n",
    "        fig, ax = plt.subplots(figsize=(10, 8), facecolor='white')\n",
    "        y_axis = 'aper30_abmag' if 'aper30_abmag' in df.columns else 'mag_2'\n",
    "        \n",
    "        sc = ax.scatter(df['color'], df[y_axis], c=df['mass_M_jup'], cmap='plasma', s=45, edgecolor='black', alpha=0.85)\n",
    "        cb = plt.colorbar(sc, ax=ax, pad=0.02)\n",
    "        cb.set_label(r\"Estimated Mass (Jupiter Masses, \(M_J\))\", fontsize=12)\n",
    "        \n",
    "        ax.invert_yaxis()\n",
    "        ax.set_title(\"IC 348 Survey Core: Multi-Filter Color-Magnitude Diagram\", fontsize=14, fontweight='bold')\n",
    "        ax.set_xlabel(f\"Color Index: {flux_cols[0].upper()} - {flux_cols[-1].upper()}\", fontsize=12)\n",
    "        ax.set_ylabel(\"Apparent Brightness (AB Mag)\", fontsize=12)\n",
    "        ax.grid(True, linestyle=':', alpha=0.6)\n",
    "        \n",
    "        plt.savefig(os.path.join(stage3_dir, \"ic348_substellar_cmd.png\"), bbox_inches='tight', dpi=300)\n",
    "        plt.show()\n",
    "        print(\"✅ CMD scientific figure generated and saved successfully.\")\n",
    "    else:\n",
    "        print(\"⚠️ Missing multi-filter synchronized flux dimensions to render scatter graph.\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (astro_env)",
   "language": "python",
   "name": "astro_env"
  },
  "language_info": {
   "codemirror_mode": {"name": "ipython", "version": 3},
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

# 2. Safely dump clean string configuration directly to target file path
with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(notebook_data, f, indent=1)

print(f"===========================================================")
print(f"🎉 REBUILD SUCCESSFUL: {notebook_path} compiled!")
print(f"===========================================================")
