# JWST Stages pipeline for analyse data

## Stage Prepare

1. Download files `_asn.json`
2. Download files `_csv.json`
3. Download files `_uncal.fits`
4. Setup Jupiter Notebook

```
(astro_env) bash> export MAST_API_TOKEN="YOUR_MAST_API_TOKENS"
>>> exec(open("./search_jw01257-o003_20260714t164831.py").read())
>>> exec(open("./search_jw01257-o003_20260714t164831_00002.py").read())
>>> exec(open("./search_jw01257-o003_20260714t164831_00005.py").read())
>>> exec(open("./search_jw01257-o003_20260714t164831_00007.py").read())
>>> exec(open("./search_jw01257-o003_20260714t164831_00008.py").read())
>>> exec(open("./search_jw01257-o003_20260714t164831_00009.py").read())
```

We have a next directories:

```
bash> cd $HOME/data_jwst/jwst-pipeline-brown-dwarf-candidates-ic348/processed_stage1_raw/
mastDownload/
└── JWST
    ├── jw01257003001_02101_00001_nrca1
    │   └── jw01257_20260714t164831_pool.csv
    ├── jw01257-o003_t005_nircam_f150w2-f162m
    │   └── jw01257-o003_20260714t164831_image3_00002_asn.json
    ├── jw01257-o003_t005_nircam_f322w2-f323n
    │   └── jw01257-o003_20260714t164831_image3_00005_asn.json
    ├── jw01257-o003_t005_nircam_f444w-f466n
    │   └── jw01257-o003_20260714t164831_image3_00008_asn.json
    └── jw01257-o003_t005_nircam_f444w-f470n
        └── jw01257-o003_20260714t164831_image3_00007_asn.json

7 directories, 5 files
```

There are directories for download `_uncal.fits` :

```
processed_stage1_raw/jw01257-o003_t005_nircam_f150w2-f162m
processed_stage1_raw/jw01257-o003_t005_nircam_f150w2-f164n
processed_stage1_raw/jw01257-o003_t005_nircam_f322w2-f323n
processed_stage1_raw/jw01257-o003_t005_nircam_f444w-f466n
processed_stage1_raw/jw01257-o003_t005_nircam_f444w-f470n
```

**Please edit are scripts: `run_batch_download.py, run_parallel_download.py`**

*Option 1: Sequential Automated Bash Loop (Recommended & Safe)*

This script loops through your various filter directories, dynamically finds
the `.json` association file inside each, and calls your
`download_asn_members.py` file one folder at a time. It keeps logs clean and
organized.

Edit file with your parameters then run `run_batch_download.sh` in the root
of your project:

```
bash> export MAST_API_TOKEN="YOUR_MAST_API_TOKENS"
bash> ./run_batch_download.sh
```

*Option 2: Parallelized Background Stream Script (Fastest)*

If you have a high-speed network connection and want to download multiple
filters at the exact same time, you can tell Bash to fork the python script
calls into background jobs using the `&` operator, and then use wait to hold
the terminal until everything is completely finished.


Edit file with your parameters and run it: `run_parallel_download.sh`

*Option 3: None Parallelized Script (Custom & Slow)*


You can now freely stack your shell commands: `download_asn_members.py`

```
# Example A: Standard baseline processing (Uses default Program 1257 and default directory)
python download_asn_members.py jw01257-o003_20260714t164831_image3_00002_asn.json

# Example B: Custom folder routing (Targets Program 1257, but forces data to local directory)
python download_asn_members.py jw01257-o003_20260714t164831_image3_00002_asn.json 1257 ./raw_uncal_pool/

# Example C: Complete override profile (Swaps program mapping and designates specific target structure)
python download_asn_members.py jw02731-o001_image3_asn.json 2731 ./external_field_data/
```

Copy and paste this multi-line sequence directly into your active Python
interactive loop or terminal console session:

```
import sys

# 1. Manually configure the input parameters (mocking sys.argv)
# Index 0 must always be the script name, followed by your custom switches
sys.argv = [
    "./download_asn_members.py",                          # Parameter 0: Script Name
    "jw01257-o003_20260714t164831_image3_00002_asn.json", # Parameter 1: ASN Filename
    "1257",                                               # Parameter 2: Proposal ID
    "./raw_uncal_pool/"                                   # Parameter 3: Destination Folder
]

# 2. Execute the script file contextually inside the environment
exec(open("./download_asn_members.py").read())
```

```
>>> exec(open("./run_stage_1_pipeline.py").read())
Reading exposure map from: ./processed_stage1_raw/mastDownload/JWST/jw01257-o003_t005_nircam_f150w2-f162m/jw01257-o003_20260714t164831_image3_00002_asn.json
Found 32 unique raw exposure members to fetch.
Querying MAST product catalog for Program 1257...
Matched 32 files out of 32 requested members inside the archive.

Starting batch download of member files...
Downloading URL
https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:JWST/product/jw01257003001_02109_00003_nrcb3_uncal.fits
...

```

output:

```
All downloads finalized successfully!
                                          Local Path                                                                                                           Status   Message URL
-------------------------------------------------------------------------------------------------------------------------------------------------------------- -------- ------- ----
./processed_stage1_raw/jw01257-o003_t005_nircam_f444w-f470n/mastDownload/JWST/jw01257003001_02103_00001_nrcalong/jw01257003001_02103_00001_nrcalong_uncal.fits COMPLETE  None   None

...
```

## Stage 1 Detector1Pipeline calibration `run_stage_1_pipeline.py`

```
bash> export CRDS_SERVER_URL="https://jwst-crds.stsci.edu"
bash> export CRDS_PATH="$HOME/crds_cache"
(astro_env) # python
Python 3.14.7 (main, Aug 10 2026, 07:46:56) [GCC 16.1.1 20260728] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exec(open("./run_stage_2_pipeline.py").read())
Located 32 raw files for pipeline processing.
Located 32 raw files for pipeline processing.

==========================================
Processing: jw01257003001_02109_00002_nrcb1_uncal.fits
==========================================
--- Running Stage 1: Detector Processing ---

...

2026-10-05 22:10:13,360 - stpipe.pipeline - INFO - Prefetching reference files for dataset: 'jw01257003001_02109_00002_nrcb1_uncal.fits' reftypes = ['dark', 'gain', 'linearity', 'mask', 'readnoise', 'refpix', 'reset', 'rscd', 'saturation', 'sirskernel', 'superbias']

...

2026-10-06 01:10:48,945 - stpipe.step - INFO - Saved model in ./processed_stage2/jw01257003001_02109_00002_nrcb3_cal.fits
2026-10-06 01:10:48,945 - stpipe.step - INFO - Step Image2Pipeline done
2026-10-06 01:10:48,946 - jwst.stpipe.core - INFO - Results used jwst version: 3.0.0

Processing complete! All exposures converted to *_cal.fits.
```

### 6 Oct 2026 by Oleg G.Kapranov
