import os
import glob

# STEP 1: DEFINE ENVIRONMENT ROUTING FIRST
os.environ["CRDS_SERVER_URL"] = "https://jwst-crds.stsci.edu"
os.environ["CRDS_PATH"] = os.path.expanduser("~/crds_cache")
os.environ["CRDS_CONTEXT"] = "jwst_1584.pmap"  # Pin the stable operational context

# STEP 2: NOW IMPORT PIPELINE ENGINES
from jwst.pipeline import Image2Pipeline
