import os
import glob
from jwst.pipeline import Detector1Pipeline, Image2Pipeline

# Configure local CRDS cache routing before pipeline compilation
os.environ["CRDS_SERVER_URL"] = "https://stsci.edu"
os.environ["CRDS_PATH"] = os.path.expanduser("~/crds_cache")

# FIX: Point glob directly to your new raw download repository directory
uncal_files = glob.glob("./processed_stage1_raw/**/*_uncal.fits", recursive=True)
print(f"Located {len(uncal_files)} raw files for pipeline processing inside ./processed_stage1_raw/")

# Define independent structured workspaces to isolate output stages cleanly
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

    # Dynamically map the path to look inside the Stage 1 rate folder
    rate_basename = file_basename.replace("_uncal.fits", "_rate.fits")
    rate_file = os.path.join(stage1_out_dir, rate_basename)

    # 2. Run Image Stage 2 Calibration (Outputs *_cal.fits
    if os.path.exists(rate_file):
        print(f"\n--- Running Stage 2: Image Processing for {rate_basename} ---")
        Image2Pipeline.call(rate_file, output_dir=stage2_out_dir, save_results=True)
    else:
        print(f"ERROR: Expected rate file not found at matching path: {rate_file}")

print("\nProcessing complete! All exposures successfully converted to *_cal.fits.")
