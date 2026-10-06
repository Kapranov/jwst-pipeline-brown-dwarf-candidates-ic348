import os
import glob
import shutil

# 1. Define paths
root_mast_dir = "./processed_stage1_raw/mastDownload/JWST"
filter_base_dir = "./processed_stage1_raw"

# Find all loose exposure folders in the root mastDownload layout
loose_exposure_dirs = [
    d for d in glob.glob(os.path.join(root_mast_dir, "jw*"))
    if os.path.isdir(d) and not os.path.basename(d).startswith("jw01257-o003_t005")
]
print(f"Found {len(loose_exposure_dirs)} loose exposure folders to sort.")

# 2. Map and move exposures to their respective filter folders based on file signatures
for exp_dir in loose_exposure_dirs:
    dir_name = os.path.basename(exp_dir)

    # Identify target filter path based on program IDs and observation rules
    if "_02109_" in dir_name:
        target_filter = "jw01257-o003_t005_nircam_f150w2-f162m"
    elif "_02101_" in dir_name and any(ch in dir_name for ch in ["nrca1", "nrca2", "nrca3", "nrca4", "nrcb1", "nrcb2", "nrcb3", "nrcb4"]):
        target_filter = "jw01257-o003_t005_nircam_f150w2-f164n"
    elif "_02105_" in dir_name:
        target_filter = "jw01257-o003_t005_nircam_f322w2-f323n"
    elif "_02101_" in dir_name and "long" in dir_name:
        target_filter = "jw01257-o003_t005_nircam_f444w-f466n"
    elif "_02103_" in dir_name:
        target_filter = "jw01257-o003_t005_nircam_f444w-f470n"
    else:
        print(f"Skipping unrecognized folder layout signature: {dir_name}")
        continue

    destination_path = os.path.join(filter_base_dir, target_filter, "mastDownload", "JWST", dir_name)
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)

    # Move the directory securely
    if not os.path.exists(destination_path):
        shutil.move(exp_dir, destination_path)
        print(f" -> Moved {dir_name} securely to {target_filter}")
    else:
        print(f" -> Destination path already exists, skipping: {dir_name}")

print("\n==========================================")
print("DIRECTORY RE-ALIGNMENT COMPLETE")
print("==========================================")

