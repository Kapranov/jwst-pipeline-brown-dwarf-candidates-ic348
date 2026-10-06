import os
import glob
from jwst.pipeline import Detector1Pipeline

# Specify your 5 target filter paths explicitly
target_filter_paths = [
    "./processed_stage1_raw/jw01257-o003_t005_nircam_f150w2-f162m/mastDownload/JWST",
    "./processed_stage1_raw/jw01257-o003_t005_nircam_f150w2-f164n/mastDownload/JWST",
    "./processed_stage1_raw/jw01257-o003_t005_nircam_f322w2-f323n/mastDownload/JWST",
    "./processed_stage1_raw/jw01257-o003_t005_nircam_f444w-f466n/mastDownload/JWST",
    "./processed_stage1_raw/jw01257-o003_t005_nircam_f444w-f470n/mastDownload/JWST"
]

# Gather files exclusively from your chosen directories
uncal_files = []
for folder in target_filter_paths:
    if os.path.exists(folder):
        found_files = glob.glob(os.path.join(folder, "**/*_uncal.fits"), recursive=True)
        uncal_files.extend(found_files)

print(f"Located {len(uncal_files)} raw files for structured pipeline processing.")

# Create clean unified directory for outputs
output_dir = "./processed_stage2/"
os.makedirs(output_dir, exist_ok=True)
# Loop and run your pipeline over the uncal_files list...
for uncal_file in uncal_files:
    # (Rest of your processing code continues the same)
    pass
