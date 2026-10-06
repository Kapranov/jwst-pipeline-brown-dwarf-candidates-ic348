import os
import glob
from jwst.pipeline import Detector1Pipeline, Image2Pipeline

# FIX: Configure local CRDS cache routing before pipeline compilation
os.environ["CRDS_SERVER_URL"] = "https://jwst-crds.stsci.edu"
os.environ["CRDS_PATH"] = os.path.expanduser("~/crds_cache")

# ... rest of your script remains exactly the same ...
uncal_files = glob.glob("./mastDownload/JWST/**/*_uncal.fits", recursive=True)
print(f"Located {len(uncal_files)} raw files for pipeline processing.")

# Locating all the downloaded uncal files recursively
uncal_files = glob.glob("./mastDownload/JWST/**/*_uncal.fits", recursive=True)
print(f"Located {len(uncal_files)} raw files for pipeline processing.")

# Define an output directory to keep your workspace organized
output_dir = "./processed_stage2/"
os.makedirs(output_dir, exist_ok=True)

for uncal_file in uncal_files:
    print(f"\n==========================================")
    print(f"Processing: {os.path.basename(uncal_file)}")
    print(f"==========================================")

    # 1. Run Detector Stage 1 Calibration (Outputs *_rate.fits)
    print("--- Running Stage 1: Detector Processing ---")
    det1_output = Detector1Pipeline.call(uncal_file, output_dir=output_dir, save_results=True)

    # Track down the dynamically generated _rate.fits output file path
    base_name = os.path.basename(uncal_file).replace("_uncal.fits", "_rate.fits")
    rate_file = os.path.join(output_dir, base_name)

    # 2. Run Image Stage 2 Calibration (Outputs *_cal.fits)
    if os.path.exists(rate_file):
        print("\n--- Running Stage 2: Image Processing ---")
        Image2Pipeline.call(rate_file, output_dir=output_dir, save_results=True)
    else:
        print(f"ERROR: Expected rate file not found at {rate_file}")

print("\nProcessing complete! All exposures converted to *_cal.fits.")
