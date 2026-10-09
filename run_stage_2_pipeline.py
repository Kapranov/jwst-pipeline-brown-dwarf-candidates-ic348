import os
import glob

# STEP 1: CONFIGURE ALL CRDS ENVIRONMENT CONFIGURATIONS FIRST (MUST PRECEED PIPELINE IMPORTS)
os.environ["CRDS_SERVER_URL"] = "https://jwst-crds.stsci.edu"
os.environ["CRDS_PATH"] = os.path.expanduser("~/crds_cache")
os.environ["CRDS_CONTEXT"] = "jwst_1584.pmap"  # Locks down local rule verification mapping

# STEP 2: NOW IMPORT THE JWST PIPELINE ENGINE COMPONENTS SAFELY
from jwst.pipeline import Detector1Pipeline, Image2Pipeline

# Scan your new raw data repository path recursively across all filters
uncal_files = glob.glob("./processed_stage1_raw/**/*_uncal.fits", recursive=True)
print(f"Located {len(uncal_files)} raw files for pipeline processing inside ./processed_stage1_raw/")

# Establish dedicated, decoupled directories for step calibrations
stage1_out_dir = "./processed_stage1_rate/"
stage2_out_dir = "./processed_stage2_cal/"

os.makedirs(stage1_out_dir, exist_ok=True)
os.makedirs(stage2_out_dir, exist_ok=True)

for uncal_file in uncal_files:
    file_basename = os.path.basename(uncal_file)
    print(f"\n==========================================")
    print(f"Processing Target: {file_basename}")
    print(f"==========================================")

    # 1. Run Detector Stage 1 Calibration (Outputs *_rate.fits)
    print("--- Running Stage 1: Detector Processing ---")
    Detector1Pipeline.call(uncal_file, output_dir=stage1_out_dir, save_results=True)

    # Track down the dynamically generated _rate.fits output file path inside stage 1
    rate_basename = file_basename.replace("_uncal.fits", "_rate.fits")
    rate_file = os.path.join(stage1_out_dir, rate_basename)

    # 2. Run Image Stage 2 Calibration (Outputs *_cal.fits)
    if os.path.exists(rate_file):
        print(f"\n--- Running Stage 2: Image Processing for {rate_basename} ---")
        Image2Pipeline.call(rate_file, output_dir=stage2_out_dir, save_results=True)
    else:
        print(f"ERROR: Expected rate file not found at matching path: {rate_file}")

print("\nProcessing complete! All exposures converted to *_cal.fits inside ./processed_stage2_cal/")
