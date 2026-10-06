#!/bin/bash

# Ensure your active astronomy virtual environment is engaged
if [ -d "/home/kapranov/astro_env" ]; then
    source /home/kapranov/astro_env/bin/activate
fi

# Accept token dynamically as an argument if passed
TOKEN_ARG=$1

# Define the list of filter subfolders you want to cycle through
FILTERS=(
    "jw01257-o003_t005_nircam_f150w2-f162m"
    "jw01257-o003_t005_nircam_f150w2-f164n"
    "jw01257-o003_t005_nircam_f322w2-f323n"
    "jw01257-o003_t005_nircam_f444w-f466n"
    "jw01257-o003_t005_nircam_f444w-f470n"
)

PROPOSAL="1257"

ROOT_DIR="./mastDownload/JWST"

echo "========================================================="
echo " STARTING JWST BATCH EXPOSURE DOWNLOAD PROCESS"
echo "========================================================="

for FILTER in "${FILTERS[@]}"; do
    TARGET_PATH="${ROOT_DIR}/${FILTER}"
    echo -e "\n---------------------------------------------------------"
    echo "Checking directory: ${FILTER}"
    echo "---------------------------------------------------------"

    if [ -d "$TARGET_PATH" ]; then
        # FIX: Removed -maxdepth 1 to search recursively down the MAST directory tree structure
        ASN_FILE=$(find "$TARGET_PATH" -name "*_asn.json" -printf "%f\n" | head -n 1)

        if [ -n "$ASN_FILE" ]; then
            echo "Found Association File: ${ASN_FILE}"
            echo "Initializing target download routine..."

            OUTPUT_DIR="./processed_stage1_raw/${FILTER}/"

            # Run python framework, optionally passing the token parameter if present
            if [ -n "$TOKEN_ARG" ]; then
                python download_asn_members.py "$ASN_FILE" "$PROPOSAL" "$OUTPUT_DIR" "$TOKEN_ARG"
            elif [ -n "$MAST_API_TOKEN" ]; then
                python download_asn_members.py "$ASN_FILE" "$PROPOSAL" "$OUTPUT_DIR" "$MAST_API_TOKEN"
            else
                python download_asn_members.py "$ASN_FILE" "$PROPOSAL" "$OUTPUT_DIR"
            fi

        else
            echo "WARNING: No *_asn.json file discovered anywhere inside ${TARGET_PATH}."
        fi
    else
        echo "ERROR: Directory path ${TARGET_PATH} does not exist on disk."
    fi
done

echo -e "\n========================================================="
echo " ALL FILTER CHANNELS DOWNLOADED SUCCESSFULLY!"
echo "========================================================="
