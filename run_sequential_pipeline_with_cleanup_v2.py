import os
import glob

# The Step 5's space-conservation routine (`run_sequential_pipeline_with_cleanup.py`).
# Processing multi-filter arrays (across your five concurrent `NIRCam` setups:
# `F162M`, `F164n`, `F323n`, `F466n`, and `F470n`) sequentially while instantly
# purging the heavy intermediate `_rate.fits` cache files is a pro-level way to
# run a large survey field like `IC 348` on a local Linux machine. Your `60 GB`
# CRDS local cache looks perfectly loaded and synced under context `jwst_1584.pmap`.

# STEP 1: CONFIGURE ALL CRDS ENVIRONMENT CONFIGURATIONS FIRST
os.environ["CRDS_SERVER_URL"] = "https://stsci.edu"
os.environ["CRDS_PATH"] = os.path.expanduser("~/crds_cache")
os.environ["CRDS_CONTEXT"] = "jwst_1584.pmap"  # Keep local pmap stable

# STEP 2: IMPORT THE JWST PIPELINE ENGINE COMPONENTS SAFELY
from jwst.pipeline import Detector1Pipeline, Image2Pipeline

# STEP 3: DEFINE ALL FIVE CONCURRENT MASTER FILTER PATHS COMPLETELY
target_filter_paths = [
    "./processed_stage1_raw/jw01257-o003_t005_nircam_f150w2-f162m/mastDownload/JWST",
    "./processed_stage1_raw/jw01257-o003_t005_nircam_f150w2-f164n/mastDownload/JWST",
    "./processed_stage1_raw/jw01257-o003_t005_nircam_f322w2-f323n/mastDownload/JWST",
    "./processed_stage1_raw/jw01257-o003_t005_nircam_f444w-f466n/mastDownload/JWST",
    "./processed_stage1_raw/jw01257-o003_t005_nircam_f444w-f470n/mastDownload/JWST"
]

# Establish dedicated global output folder endpoints
stage1_out_dir = "./processed_stage1_rate/"
stage2_out_dir = "./processed_stage2_cal/"
os.makedirs(stage1_out_dir, exist_ok=True)
os.makedirs(stage2_out_dir, exist_ok=True)

print("==========================================")
print("MASTER MULTI-FILTER PIPELINE EXECUTION ENGINE")
print("==========================================\n")

# Begin Master Outer Loop traversing across all filter subdirectories
for filter_idx, filter_path in enumerate(target_filter_paths, 1):
    # Extract the descriptive directory tag name for clean console logging
    filter_tag = filter_path.split('/')[2]

    print(f"======================================================================")
    print(f"GROUP [{filter_idx}/{len(target_filter_paths)}]: Processing Directory -> {filter_tag}")
    print(f"======================================================================")

    # Locate all raw files inside the current target subfolder path layout
    uncal_files = glob.glob(os.path.join(filter_path, "*/*_uncal.fits"))

    if len(uncal_files) == 0:
        print(f" --> Skipping: No raw exposures (*_uncal.fits) located inside this sub-track.\n")
        continue

    print(f"Located {len(uncal_files)} exposure frames to clean-calibrate sequentially.\")\n")

    # Step 4: Begin Internal Sequential Ingestion Loop for the current folder
    for idx, uncal_file in enumerate(uncal_files, 1):
        file_basename = os.path.basename(uncal_file)

        print(f"  [{idx}/{len(uncal_files)}] Calibrating Exposure: {file_basename}")
        print(f"  ----------------------------------------------------------------")

        # A. Trigger Detector Stage 1 Routine (Outputs *_rate.fits and *_rateints.fits)
        print("   -> Running Stage 1: Detector Processing...")
        Detector1Pipeline.call(uncal_file, output_dir=stage1_out_dir, save_results=True)

        # Track down all dynamically generated temporary output paths inside stage 1 folder
        rate_basename = file_basename.replace("_uncal.fits", "_rate.fits")
        rate_ints_basename = file_basename.replace("_uncal.fits", "_rateints.fits")

        rate_file = os.path.join(stage1_out_dir, rate_basename)
        rate_ints_file = os.path.join(stage1_out_dir, rate_ints_basename)

        # B. Trigger Image Stage 2 Routine
        if os.path.exists(rate_file):
            print(f"   -> Running Stage 2: Calibrated Image processing for {rate_basename}...")
            Image2Pipeline.call(rate_file, output_dir=stage2_out_dir, save_results=True)

            # C. CRITICAL MULTI-SUBDIRECTORY STORAGE PURGE
            print(f"   -> Space Conservation: Cleaning temporary Stage 1 cache links...")

            if os.path.exists(rate_file):
                os.remove(rate_file)
                print(f"      Deleted temporary intermediate product: {rate_basename}")

            if os.path.exists(rate_ints_file):
                os.remove(rate_ints_file)
                print(f"      Deleted temporary intermediate product: {rate_ints_basename}")

            print("      Disk architecture footprint protected successfully.")
        else:
            print(f"   ERROR: Expected intermediate rate file not found at path: {rate_file}")

        print(f"  ----------------------------------------------------------------\n")

print("\n==========================================")
print("ALL MULTI-FILTER PIPELINE AUTOMATIONS COMPLETE!")
print(f"Science-ready calibrations stored in: {stage2_out_dir}")
print("==========================================\n")
