#!/usr/bin/env bash

# When you call calibration pipelines via python scripts, any environment
# variable parameters (`os.environ["CRDS_SERVER_URL"]`, `os.environ["CRDS_PATH"`],
# or `os.environ["CRDS_CONTEXT"]`) must be defined at the absolute top of
# the execution thread, before you import any pipeline components (like
# `Detector1Pipeline` or `Image2Pipeline`).

# CRDS (Calibration Reference Data System) works inside the jwst pipeline ecosystem.
CRDS_SERVER_URL="https://jwst-crds.stsci.edu" CRDS_PATH="/home/kapranov/crds_cache" crds sync --contexts jwst_1584.pmap
