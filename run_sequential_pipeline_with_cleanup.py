import os
import glob

# STEP 1: CONFIGURE ALL CRDS ENVIRONMENT CONFIGURATIONS FIRST (MUST PRECEED PIPELINE IMPORTS)
os.environ["CRDS_SERVER_URL"] = "https://jwst-crds.stsci.edu"
os.environ["CRDS_PATH"] = os.path.expanduser("~/crds_cache")
os.environ["CRDS_CONTEXT"] = "jwst_1584.pmap"  # Keep local rule mapping stable

# STEP 2: IMPORT THE JWST PIPELINE ENGINE COMPONENTS SAFELY
from jwst.pipeline import Detector1Pipeline, Image2Pipeline

# Target folder for your F322W2/F323N dataset
raw_data_dir = "./processed_stage1_raw/jw01257-o003_t005_nircam_f150w2-f162m/mastDownload/JWST/*"

# Find all raw uncal files inside that directory
uncal_files = glob.glob(os.path.join(raw_data_dir, "*_uncal.fits"))

if len(uncal_files) == 0:
    print(f"ERROR: No _uncal.fits files located inside {raw_data_dir}")
else:
    print(f"==========================================")
    print(f"AUTOMATED SEQUENTIAL PIPELINE WITH CLEANUP")
    print(f"Located {len(uncal_files)} files to process safely.")
    print(f"==========================================")

    # Establish dedicated outputs folders
    stage1_out_dir = "./processed_stage1_rate/"
    stage2_out_dir = "./processed_stage2_cal/"
    os.makedirs(stage1_out_dir, exist_ok=True)
    os.makedirs(stage2_out_dir, exist_ok=True)

    # Begin the disk-safe sequential execution loop
    for idx, uncal_file in enumerate(uncal_files, 1):
        file_basename = os.path.basename(uncal_file)

        print(f"\n------------------------------------------")
        print(f"[{idx}/{len(uncal_files)}] Processing Target: {file_basename}")
        print(f"------------------------------------------")

        # 1. Run Detector Stage 1 Calibration
        print("--- Running Stage 1: Detector Processing ---")
        Detector1Pipeline.call(uncal_file, output_dir=stage1_out_dir, save_results=True)

        # Track down the dynamically generated _rate.fits output file path inside stage 1
        rate_basename = file_basename.replace("_uncal.fits", "_rate.fits")
        rate_file = os.path.join(stage1_out_dir, rate_basename)

        # 2. Run Image Stage 2 Calibration
        if os.path.exists(rate_file):
            print(f"\n--- Running Stage 2: Image Processing for {rate_basename} ---")
            Image2Pipeline.call(rate_file, output_dir=stage2_out_dir, save_results=True)

            # 3. INSTANT CACHE PURGE: Wipe out the heavy intermediate file before the next iteration
            print(f"\n--- Stage 5 Space Conservation: Purging intermediate file ---")
            os.remove(rate_file)
            print(f"Successfully deleted temporary file: {rate_file}")
            print("Disk space protected successfully.")
        else:
            print(f"ERROR: Expected rate file not found at matching path: {rate_file}")

    print("\n==========================================")
    print("SEQUENTIAL MULTI-FILE WORKFLOW COMPLETE!")
    print(f"All outputs stored inside: {stage2_out_dir}")
    print("==========================================\n")
