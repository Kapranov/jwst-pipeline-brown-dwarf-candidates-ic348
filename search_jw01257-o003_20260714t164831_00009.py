from astroquery.mast import Observations

Observations.login(token="268b72a1bcf2473fa21cea468ebf30d5")

# 1. Query by the JWST collection and specific Proposal/Program ID (1257)
obs_table = Observations.query_criteria(obs_collection="JWST", proposal_id="1257")

print(f"Found {len(obs_table)} observations for program 1257. Fetching all products...")

# 2. Get the full list of products (including auxiliary and engineering tables)
products = Observations.get_product_list(obs_table)

# 3. Filter down exclusively to your target pool file string
target_pool = "jw01257-o003_20260714t164831_image3_00009_asn.json"
matching_file = products[products['productFilename'] == target_pool]

# 4. Check if the file is available and download it
if len(matching_file) > 0:
    print(f"File found! Initiating download for {target_pool}...")
    # Make sure to check your physical label/token permissions if it is restricted data
    Observations.download_products(matching_file)
else:
    print(f"Could not find {target_pool} directly. Checking alternative types...")
    # Look for any association pool tables matching this program's run date
    pool_files = products[products['productFilename'].str.contains('_asn.json', na=False)]
    print("Available association pools in this program:")
    print(pool_files['productFilename'])
