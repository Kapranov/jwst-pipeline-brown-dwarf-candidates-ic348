import os
import glob
import json
from astropy.io import fits
from jwst.pipeline import Image3Pipeline

# 1. Anchor environment parameters
os.environ["CRDS_SERVER_URL"] = "https://stsci.edu"
os.environ["CRDS_PATH"] = os.path.expanduser("~/crds_cache")
os.environ["CRDS_CONTEXT"] = "jwst_1584.pmap"

stage2_dir = "./processed_stage2_cal/"
stage3_dir = "./processed_stage3/"
os.makedirs(stage3_dir, exist_ok=True)

print("==========================================")
print("LAUNCHING STAGE 3 MULTI-FILTER MOSAIC LOOP")
print("==========================================\n")

# 2. Gather all science-calibrated exposures (*_cal.fits)
all_cal_files = glob.glob(os.path.join(stage2_dir, "*_cal.fits"))

if len(all_cal_files) == 0:
    print(f"ERROR: No calibrated exposure files found inside {stage2_dir}")
else:
    # Group exposures dynamically by their metadata headers to handle all 5 configurations
    filter_groups = {}

    print(f"Sorting {len(all_cal_files)} calibrated files into unique filter tracks...")
    for filepath in all_cal_files:
        abs_filepath = os.path.abspath(filepath)
        try:
            with fits.open(abs_filepath) as hdul:
                header = hdul[0].header
                # Combine FILTER and PUPIL to isolate unique tracking frames (e.g., F150W2_F162M)
                filter_key = f"{header.get('FILTER')}_{header.get('PUPIL')}"

            if filter_key not in filter_groups:
                filter_groups[filter_key] = []
            filter_groups[filter_key].append(abs_filepath)
        except Exception as e:
            print(f"Warning: Skipping corrupted frame {os.path.basename(filepath)}: {e}")

    # 3. Iterate sequentially over each isolated filter configuration channel
    for filter_idx, (filter_name, file_list) in enumerate(filter_groups.items(), 1):
        print(f"\n----------------------------------------------------------------------")
        print(f"PROCESSING TRACK [{filter_idx}/{len(filter_groups)}]: Filter Band -> {filter_name}")
        print(f"Associated exposures found for stacking: {len(file_list)}")
        print(f"----------------------------------------------------------------------")

        # Generate compliant Level 3 Association schema mapping for this specific band
        asn_data = {
            "asn_rule": "Candidate_Asn",
            "asn_pool": "none",
            "program": "01257",
            "asn_type": "image3",
            "products": [
                {
                    "name": f"hh211_stacked_mosaic_{filter_name.lower()}",
                    "members": [{"expname": fp, "exptype": "science"} for fp in file_list]
                }
            ]
        }

        # Write clean JSON tracking specification
        asn_filename = os.path.abspath(os.path.join(stage3_dir, f"association_stage3_{filter_name.lower()}_asn.json"))
        with open(asn_filename, "w") as f:
            json.dump(asn_data, f, indent=4)
        print(f" -> Level 3 Association file structured safely at: {os.path.basename(asn_filename)}")

        # 4. Trigger Image3Pipeline combination loop
        print(f" -> Invoking Image3Pipeline combination sequence for {filter_name}...")
        try:
            Image3Pipeline.call(asn_filename, output_dir=stage3_dir, save_results=True)
            print(f" -> SUCCESS: Aligned science mosaic ready for track {filter_name}.")
        except Exception as e:
            print(f" -> PIPELINE CRASH executing group {filter_name}: {e}")

    print("\n==========================================")
    print("STAGE 3 MULTI-FILTER MOSAIC LOOP VERIFIED!")
    print(f"All stacked mosaics stored in: {stage3_dir}")
    print("==========================================\n")
