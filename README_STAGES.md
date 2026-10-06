# JWST Stages pipeline for analyse data

## Stage 0

1. Download files `_asn.json`
2. Download files `_csv.json`
3. Prepare setup Jupiter Notebook

## Stage 1

```
>>> exec(open("./run_stage_1_pipeline.py").read())
Reading exposure map from: ./mastDownload/JWST/jw01257-o003_t005_nircam_f150w2-f162m/jw01257-o003_20260714t164831_image3_00002_asn.json
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
                                          Local Path                                            Status  Message URL
---------------------------------------------------------------------------------------------- -------- ------- ----
./mastDownload/JWST/jw01257003001_02109_00003_nrcb3/jw01257003001_02109_00003_nrcb3_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00004_nrcb4/jw01257003001_02109_00004_nrcb4_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00004_nrcb3/jw01257003001_02109_00004_nrcb3_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00004_nrcb2/jw01257003001_02109_00004_nrcb2_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00003_nrca1/jw01257003001_02109_00003_nrca1_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00004_nrcb1/jw01257003001_02109_00004_nrcb1_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00003_nrca3/jw01257003001_02109_00003_nrca3_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00004_nrca4/jw01257003001_02109_00004_nrca4_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00004_nrca3/jw01257003001_02109_00004_nrca3_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00003_nrca4/jw01257003001_02109_00003_nrca4_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00003_nrca2/jw01257003001_02109_00003_nrca2_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00004_nrca1/jw01257003001_02109_00004_nrca1_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00003_nrcb4/jw01257003001_02109_00003_nrcb4_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00004_nrca2/jw01257003001_02109_00004_nrca2_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00003_nrcb2/jw01257003001_02109_00003_nrcb2_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00003_nrcb1/jw01257003001_02109_00003_nrcb1_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00002_nrca3/jw01257003001_02109_00002_nrca3_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00001_nrca2/jw01257003001_02109_00001_nrca2_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00002_nrcb3/jw01257003001_02109_00002_nrcb3_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00002_nrcb1/jw01257003001_02109_00002_nrcb1_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00001_nrcb4/jw01257003001_02109_00001_nrcb4_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00002_nrcb2/jw01257003001_02109_00002_nrcb2_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00002_nrca1/jw01257003001_02109_00002_nrca1_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00002_nrca2/jw01257003001_02109_00002_nrca2_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00001_nrca1/jw01257003001_02109_00001_nrca1_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00001_nrcb2/jw01257003001_02109_00001_nrcb2_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00002_nrcb4/jw01257003001_02109_00002_nrcb4_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00001_nrcb3/jw01257003001_02109_00001_nrcb3_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00001_nrcb1/jw01257003001_02109_00001_nrcb1_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00001_nrca4/jw01257003001_02109_00001_nrca4_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00002_nrca4/jw01257003001_02109_00002_nrca4_uncal.fits COMPLETE    None None
./mastDownload/JWST/jw01257003001_02109_00001_nrca3/jw01257003001_02109_00001_nrca3_uncal.fits COMPLETE    None None
```

## Stage 2

```
```

### 6 Oct 2026 by Oleg G.Kapranov

