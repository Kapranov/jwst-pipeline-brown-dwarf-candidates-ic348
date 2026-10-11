# JWST Multiphase Science Pipeline & Analysis Tracker

**Target Regions:** IC 348 Brown Dwarf Cluster Core & HH 211 Protostellar Outflow
**PI Designation:** Oleg G. Kapranov
**Date/Version:** October 2026 (Pipeline Stage 3 Ready)
**Instrument System:** JWST NIRCam (Broad & Narrow Filter Configurations)

---

## 🌌 Core Science Tasks

### 1. Multi-Filter Color-Magnitude Diagram (CMD) Construction
* **Objective:** Map effective temperatures and trace atmospheric dust structures for discovered substellar candidates.
* **Methodology:** Cross-match the exact pixel spatial coordinates of the **205 brown dwarf candidates** isolated from the broad-band `F444W` filter against short-wave calibrations (`F150W2` or `F322W2`). 
* **Key Metric:** Compute color indexes (e.g., \([F150W2] - [F444W]\)) to evaluate structural youth cooling sequences.

### 2. Narrow-Band Gas Continuum Extinction (\(A_V\))
* **Objective:** Calculate localized gas extinction values directly across cluster stars.
* **Methodology:** Utilize companion narrow-band filtering layers (`F164N` Paschen-alpha / continuum or `F470N`) to gauge if candidates remain deeply embedded inside the molecular cloud cores of the Perseus complex.

---

## 🗺️ Spectral Band Matrix Reference

This operational matrix maps out your multi-filter data tracking across your repository channels:

| Short-Wave Baseline Filter | Narrow-Band Gas/Dust Filter | Target Emission Science | Intrinsic Property Revealed |
| :--- | :--- | :--- | :--- |
| **F150W2** (Broad-band) | `F162M` / `F164N` | Continuum & [Fe II] Iron Lines | High-velocity protostellar shocks |
| **F322W2** (Broad-band) | `F323N` | Molecular Hydrogen (H₂) | Hot shocked gas filaments |
| **F444W** (Broad-band) | `F466N` / `F470N` | Carbon Monoxide (CO) / H₂ | Entrained molecular outflows |

---

## 🛠️ Data Reduction Progression Steps

### Stage 1 (`calwebb_image1`) & Stage 2 (`calwebb_image2`) — [COMPLETED]
* Raw sensor outputs have been fully corrected, calibrated into individual exposures (`*_cal.fits`), and cross-checked via `jwst` pipeline version `3.0.0` using the `jwst_1584.pmap` CRDS tracking context.

### Stage 3 (`calwebb_image3`) — [READY TO EXECUTE]
* **Goal:** Co-add individual dither exposures into stacked, high-contrast scientific images.
* **Required Inputs:** Level 3 Association JSON configuration mappings (`*_asn.json`) pointing to absolute directory paths of raw `*_cal.fits` files. *(Do not pass Stage 2 resampled `_i2d.fits` files for scientific stacking).*
* **Pipeline Enhancements:** Astrometric drift fixes via `TweakReg`, cosmic ray outlier filtering (`*_crf.fits`), background sky matching, object segmentation pixel grids (`*_segm.fits`), and final catalog generation (`*_cat.ecsv`).

---

## 📂 Project Directory Architecture Layout

Below is the verified layout for manual file tracking across your environment subdirectories:

```text
://github.com
├── processed_stage2_cal/                      # Baseline Input calibration files
│   └── *_cal.fits                             # Standard individual calibrated exposures
└── processed_stage3/                          # Target science layer outputs (~18 GB)
    ├── association_stage3_*_asn.json          # Target Level 3 Association blueprints
    ├── hh211_stacked_mosaic_*_i2d.fits        # Science-ready co-added stacked mosaics
    ├── hh211_stacked_mosaic_*_segm.fits       # Extracted object segmentation arrays
    ├── hh211_stacked_mosaic_*_cat.ecsv        # Aperture source catalogs per filter
    ├── *_crf.fits                             # Cosmic ray flagged exposure layers
    ├── ic348_brown_dwarf_candidates_final.csv # Isolated 205 core discovery target index
    ├── ic348_combined_master_science_catalog.csv # Synchronized multi-band forced flux matrix
    └── ic348_substellar_cmd.png               # Final scientific color-magnitude scatter output
```

### 10 Oct 2026 by Oleg G.Kapranov
