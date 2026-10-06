import os
import sys
from astroquery.mast import Observations

# 1. Flexible Authentication Routine via Environment Variables
# Safely pull your fresh token from the Linux environment matrix
mast_token = os.environ.get("MAST_API_TOKEN", "").strip()

if not Observations.authenticated():
    if mast_token:
        print(f"Authenticating with environment token (Length: {len(mast_token)})...")
        try:
            Observations.login(token=mast_token)
            print("Authentication Successful!")
        except Exception as e:
            print(f"Authentication Failed: {e}")
            print("Attempting to proceed anonymously for public archival data...")
    else:
        print("No MAST_API_TOKEN detected in environment variables.")
        print("Proceeding anonymously for public database access...")

# 2. Query by the JWST collection and specific Proposal/Program ID (1257)
proposal_id = "1257"
obs_table = Observations.query_criteria(obs_collection="JWST", proposal_id=proposal_id)
print(f"Found {len(obs_table)} observations for program {proposal_id}. Fetching product metadata tree...")

# Get the full list of products
products = Observations.get_product_list(obs_table)

# 3. Filter down exclusively to your target pool file string
target_pool = "jw01257_20260714t164831_pool.csv"
matching_file = products[products['productFilename'] == target_pool]

# Establish and create the new target raw input workspace directory
output_raw_dir = "./processed_stage1_raw/"
os.makedirs(output_raw_dir, exist_ok=True)

# 4. Check if the file is available and download it directly to your new folder path
if len(matching_file) > 0:
    print(f"\nTarget File Isolated! Initiating download for: {target_pool}")
    print(f"Output Destination: {os.path.abspath(output_raw_dir)}")

    # Overriding download_dir routes the file straight into your target path
    manifest = Observations.download_products(matching_file, download_dir=output_raw_dir)
    print("\nDownload complete! Manifest receipt summarized below:")
    print(manifest)
else:
    print(f"\nCould not find {target_pool} directly. Checking alternative types...")
    # Look for any association pool tables matching this program's run date
    pool_files = products[products['productFilename'].str.contains('_pool.csv', na=False)]
    print("\nAvailable association pools found in this program:")
    print(pool_files['productFilename'])
