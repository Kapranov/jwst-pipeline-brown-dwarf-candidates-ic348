import os
import glob

# STEP 1: CONFIGURE ALL CRDS ENVIRONMENT CONFIGURATIONS FIRST (MUST PRECEED PIPELINE IMPORTS)
os.environ["CRDS_SERVER_URL"] = "https://jwst-crds.stsci.edu"
os.environ["CRDS_PATH"] = os.path.expanduser("~/crds_cache")
os.environ["CRDS_CONTEXT"] = "jwst_1584.pmap"  # Keep local rule mapping stable

# STEP 2: IMPORT THE JWST PIPELINE ENGINE COMPONENTS SAFELY
from jwst.pipeline import Detector1Pipeline, Image2Pipeline

# Target folder for your F470N dataset
raw_data_dir = "./processed_stage1_raw/jw01257-o003_t005_nircam_f444w-f470n/*/*/*"

# Find all uncal files in that directory
uncal_files = glob.glob(os.path.join(raw_data_dir, "*_uncal.fits"))

if len(uncal_files) == 0:
    print(f"ERROR: No _uncal.fits files found inside {raw_data_dir}")
    print("Please make sure you have placed your raw file inside that folder.")
else:
    # CRITICAL STAGE 5 DISK CONSTRAINT: Force selection of ONLY ONE file
    target_uncal_file = os.path.abspath(uncal_files[0])
    file_basename = os.path.basename(target_uncal_file)

    print("\n==========================================")
    print("STAGE 5 DISK-SAFE RUN INITIATED")
    print(f"Isolated single file: {file_basename}")
    print("==========================================")

    # Establish dedicated outputs directories
    stage1_out_dir = "./processed_stage1_rate/"
    stage2_out_dir = "./processed_stage2_cal/"
    os.makedirs(stage1_out_dir, exist_ok=True)
    os.makedirs(stage2_out_dir, exist_ok=True)

    # 1. Run Detector Stage 1 Calibration
    print("\n--- Running Stage 1: Detector Processing ---")
    Detector1Pipeline.call(target_uncal_file, output_dir=stage1_out_dir, save_results=True)

    # Construct expected intermediate rate path
    rate_basename = file_basename.replace("_uncal.fits", "_rate.fits")
    rate_file = os.path.join(stage1_out_dir, rate_basename)

    # 2. Run Image Stage 2 Calibration
    if os.path.exists(rate_file):
        print(f"\n--- Running Stage 2: Image Processing for {rate_basename} ---")
        Image2Pipeline.call(rate_file, output_dir=stage2_out_dir, save_results=True)

        # 3. CRITICAL STORAGE CLEANUP: Purge the intermediate _rate.fits to save massive space
        print(f"\n--- Stage 5 Space Conservation: Purging intermediate file ---")
        os.remove(rate_file)
        print(f"Successfully deleted temporary file: {rate_file}")
        print("Disk space protected successfully.")
    else:
        print(f"ERROR: Expected rate file not found at matching path: {rate_file}")

    print("\n==========================================")
    print("STAGE 5 VERIFICATION COMPLETE!")
    print(f"Your calibrated exposure is safe inside: {stage2_out_dir}")
    print("==========================================\n")
