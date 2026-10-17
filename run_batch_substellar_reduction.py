"""
JWST Multiphase Data Reduction: Automated Batch Processing Loop
Author: Oleg G. Kapranov
Version: 4.2.0 (SIMD Production Batch Release)
"""

import os
import numpy as np
import pandas as pd
from core_reduction_engine import VectorReductionEngine, process_differential_line_excess
from sigma_clip_variance_tracker import VectorSigmaClipper

def run_production_pipeline_batch(mosaic_fits_path, candidate_catalog_csv, output_catalog_csv):
    print("======================================================================")
    echo_string = f"INITIALIZING VECTOR PIPELINE AUTOMATION: BATCH DATA REDUCTION RUN"
    print(echo_string)
    print("======================================================================\n")

    # 1. Initialize data extraction pipelines and catalog coordinate arrays
    if not os.path.exists(mosaic_fits_path) or not os.path.exists(candidate_catalog_csv):
        print("❌ Execution Aborted: Missing necessary scientific input catalogs or FITS mosaics.")
        return

    print("🛰️ Step 1: Loading Stage 3 mosaic extensions and target registries...")
    engine = VectorReductionEngine(mosaic_fits_path)
    clipper = VectorSigmaClipper(sigma_threshold=3.0, max_iterations=5)
    df = pd.read_csv(candidate_catalog_csv)

    print(f"   --> Found {len(df)} target nodes inside the catalog matrix mapping.")

    # ==========================================================================
    # 🗺️ Step 2: Executing vectorized astrometric transformation array loops...
    # ==========================================================================
    print("\n🗺️ Step 2: Executing vectorized astrometric transformation array loops...")

    # Dynamically match column headers to capture variations like RA_deg/Dec_deg
    if 'ra' in df.columns: ra_col = 'ra'
    elif 'RA' in df.columns: ra_col = 'RA'
    elif 'RA_deg' in df.columns: ra_col = 'RA_deg'
    else: ra_col = 'RA_deg' # default fallback mapping key

    if 'dec' in df.columns: dec_col = 'dec'
    elif 'Dec' in df.columns: dec_col = 'Dec'
    elif 'Dec_deg' in df.columns: dec_col = 'Dec_deg'
    else: dec_col = 'Dec_deg'

    if ra_col not in df.columns or dec_col not in df.columns:
        print("❌ Error: Could not locate coordinate headers (RA/Dec) inside the CSV columns.")
        print(f"Available headers: {list(df.columns)}")
        return

    grid_x, grid_y = engine.vectorized_celestial_to_grid(df[ra_col], df[dec_col])
    df['Grid_X'] = grid_x
    df['Grid_Y'] = grid_y

    # 3. Vectorized background and noise estimation
    print("\n🌋 Step 3: Running vectorized sigma-clipped background noise extraction...")
    sky_medians, sky_variances = clipper.compute_sky_variance_vector(
        engine.data, grid_x, grid_y, background_annulus_outer=12, background_annulus_inner=6
    )
    df['Sky_Median'] = sky_medians
    df['Sky_RMS_Noise'] = sky_variances

    # 4. Forced aperture flux integration
    print("\n🎯 Step 4: Executing forced-aperture matrix flux integrations...")
    raw_flux = engine.evaluate_forced_aperture_flux(grid_x, grid_y, aperture_radius=4)

    # Calculate background subtraction via analytical vector broadcasting
    aperture_area = np.pi * (4**2)
    net_flux = raw_flux - (df['Sky_Median'].to_numpy() * aperture_area)

    # Structural self-healing safeguard preventing negative fluxes before logs
    net_flux = np.clip(net_flux, a_min=1e-5, a_max=None)
    df['Net_Aperture_Flux'] = net_flux

    # 5. Convert to standard AB Magnitudes
    print("\n✨ Step 5: Transforming arrays into standard calibrated AB Magnitudes...")
    # Checks both science and primary headers for the photometric calibration zero point
    phot_zero_point = float(engine.header.get('PHOTZP', engine.primary_header.get('PHOTZP', 28.0)))
    df['AB_Magnitude'] = -2.5 * np.log10(df['Net_Aperture_Flux']) + phot_zero_point

    # 6. Database export
    print("\n📂 Step 6: Exporting synchronized master database...")
    df.to_csv(output_catalog_csv, index=False)

    print("\n======================================================================")
    print(f"🎉 SUCCESS: BATCH RUN COMPLETE! CALIBRATED MASTER ENGINE EXPORTED.")
    print(f"💾 Production Data Saved to: {output_catalog_csv}")
    print("======================================================================")

if __name__ == "__main__":
    # Explicit file path setup matching your Arch Linux workspace architecture
    stage3_dir = "./processed_stage3/"

    # PRODUCITON FIX: Swap the placeholder PNG for your actual 1.4 GB Stage 3 FITS image file
    mosaic_path = os.path.join(stage3_dir, "hh211_stacked_mosaic_f150w2_f162m_i2d.fits")

    catalog_in = os.path.join(stage3_dir, "ic348_brown_dwarf_candidates_final.csv")
    catalog_out = os.path.join(stage3_dir, "ic348_combined_master_science_catalog.csv")

    # Run the compiled array reduction pipeline
    run_production_pipeline_batch(mosaic_path, catalog_in, catalog_out)
