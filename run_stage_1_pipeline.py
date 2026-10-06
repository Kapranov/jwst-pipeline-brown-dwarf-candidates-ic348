import json
import os
import numpy as np
from astroquery.mast import Observations

# 1. Paths configuration
asn_file_path = "./mastDownload/JWST/jw01257-o003_t005_nircam_f150w2-f162m/jw01257-o003_20260714t164831_image3_00002_asn.json"
proposal_id = "1257"

if not os.path.exists(asn_file_path):
    raise FileNotFoundError(f"Could not locate the association JSON at {asn_file_path}")

# 2. Authenticate using your active token sequence
if not Observations.authenticated():
    print("Session expired or unauthenticated. Re-logging in...")
    Observations.login(token="268b72a1bcf2473fa21cea468ebf30d5")

# 3. Parse the JSON file to find the member exposures
print(f"Reading exposure map from: {asn_file_path}")
with open(asn_file_path, "r") as f:
    asn_data = json.load(f)

# Loop through the association product matrix to collect member filenames
target_expnames = []
for product in asn_data.get("products", []):
    for member in product.get("members", []):
        expname = member.get("expname")
        if expname:
            # Clean up the extension if it already has .fits
            if expname.endswith(".fits"):
                base_name = expname.rsplit("_", 1)[0]
            else:
                base_name = expname

            # Safely build the exact uncal filename string
            uncal_filename = f"{base_name}_uncal.fits"
            target_expnames.append(uncal_filename)

# Deduplicate the list
target_expnames = list(set(target_expnames))
print(f"Found {len(target_expnames)} unique raw exposure members to fetch.")

# 4. Query MAST for the data product tree under Program 1257
print(f"Querying MAST product catalog for Program {proposal_id}...")
obs_table = Observations.query_criteria(obs_collection="JWST", proposal_id=proposal_id)
all_products = Observations.get_product_list(obs_table)

# 5. FIX: Convert the Astropy column to a NumPy array to safely check membership
filenames_array = np.array(all_products['productFilename'])
mask = np.isin(filenames_array, target_expnames)
matching_products = all_products[mask]

print(f"Matched {len(matching_products)} files out of {len(target_expnames)} requested members inside the archive.")

# 6. Execute the secure batch download
if len(matching_products) > 0:
    print("\nStarting batch download of member files...")
    manifest = Observations.download_products(matching_products)
    print("\nAll downloads finalized successfully!")
    print(manifest)
else:
    print("\nNo matching file names could be found. Here is a sample of what the script searched for:")
    for sample in target_expnames[:3]:
        print(f" - {sample}")
