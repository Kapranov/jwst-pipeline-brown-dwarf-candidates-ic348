import json
import os
import sys
import glob
import numpy as np
from astroquery.mast import Observations

# 1. Parse command-line parameters safely
if len(sys.argv) < 2:
    print("\nERROR: Missing required arguments.")
    print("Usage: python download_asn_members.py <your_asn_file.json> [proposal_id] [download_dir] [token]")
    sys.exit(1)

target_json_name = sys.argv[1]
proposal_id = str(sys.argv[2]) if len(sys.argv) >= 3 else "1257"
download_dir = os.path.abspath(sys.argv[3]) if len(sys.argv) >= 4 else None

# Check command line slot 4 first, then environmental variables
if len(sys.argv) >= 5 and sys.argv[4].strip():
    mast_token = str(sys.argv[4]).strip()
else:
    mast_token = os.environ.get("MAST_API_TOKEN", "").strip()

if download_dir:
    os.makedirs(download_dir, exist_ok=True)

mast_jwst_root = "./mastDownload/JWST/"

# Locate the target association json file
search_pattern = os.path.join(mast_jwst_root, "**", target_json_name)
found_files = glob.glob(search_pattern, recursive=True)

if not found_files:
    raise FileNotFoundError(f"ERROR: Could not locate file '{target_json_name}' under {mast_jwst_root}")

asn_file_path = os.path.abspath(found_files[0])

print(f"\n==========================================")
print(f"ENVIRONMENT CONFIGURATION ACTIVE")
print(f"==========================================")
print(f"Association File: {asn_file_path}")
print(f"MAST Program ID:  {proposal_id}")
print(f"Target Directory: {download_dir if download_dir else 'Default Cache'}")

# Mask token prefix for clear terminal diagnostic logging
if mast_token:
    print(f"Active Token:     {mast_token[:4]}...{mast_token[-4:]} (Length: {len(mast_token)})")
else:
    print(f"Active Token:     None detected")
print(f"==========================================\n")

# 2. Robust Authentication Handler
if not Observations.authenticated():
    if mast_token:
        print("Connecting to MAST Authorization Servers...")
        try:
            Observations.login(token=mast_token)
            print("Authentication Successful!")
        except Exception as e:
            print(f"\n[WARNING] Token login failed with error: {e}")
            print("Attempting to bypass security and proceed anonymously for public archival files...\n")
    else:
        print("No token provided. Proceeding anonymously for public database access...")

# 3. Parse JSON file to collect exposure names
with open(asn_file_path, "r") as f:
    asn_data = json.load(f)

target_expnames = []
for product in asn_data.get("products", []):
    for member in product.get("members", []):
        expname = member.get("expname")
        if expname:
            if expname.endswith(".fits"):
                base_name = expname.rsplit("_", 1)[0]
            else:
                base_name = expname
            target_expnames.append(f"{base_name}_uncal.fits")

target_expnames = list(set(target_expnames))
print(f"Found {len(target_expnames)} unique raw exposure members to fetch.")

# 4. Query MAST database under specified Program ID
print(f"Querying MAST product catalog for Program {proposal_id}...")
obs_table = Observations.query_criteria(obs_collection="JWST", proposal_id=proposal_id)
all_products = Observations.get_product_list(obs_table)

# 5. Filter archival database products using NumPy array processing
filenames_array = np.array(all_products['productFilename'])
mask = np.isin(filenames_array, target_expnames)
matching_products = all_products[mask]

print(f"Matched {len(matching_products)} files out of {len(target_expnames)} requested members inside the archive.")

# 6. Execute secure batch download with destination routing override
if len(matching_products) > 0:
    print("\nStarting batch download of member files...")
    if download_dir:
        manifest = Observations.download_products(matching_products, download_dir=download_dir)
    else:
        manifest = Observations.download_products(matching_products)
    print("\nAll downloads finalized successfully!")
else:
    print("\nNo matching file names could be found. Here is a sample of what the script searched for:")
    for sample in target_expnames[:3]:
        print(f" - {sample}")



