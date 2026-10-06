#!/bin/bash

if [ -d "/home/kapranov/astro_env" ]; then
    source /home/kapranov/astro_env/bin/activate
fi

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
echo " LAUNCHING PARALLEL DOWNLOADING OVERRIDE PATTERNS"
echo "========================================================="

for FILTER in "${FILTERS[@]}"; do
    TARGET_PATH="${ROOT_DIR}/${FILTER}"

    if [ -d "$TARGET_PATH" ]; then
        ASN_FILE=$(find "$TARGET_PATH" -maxdepth 1 -name "*_asn.json" -printf "%f\n" | head -n 1)

        if [ -n "$ASN_FILE" ]; then
            echo "[FORK]: Launching background thread process for ${FILTER}..."

            # The trailing '&' forks the python execution block into a concurrent parallel background worker
            python download_asn_members.py "$ASN_FILE" "$PROPOSAL" "./processed_stage1_raw/${FILTER}/" > "download_${FILTER}.log" 2>&1 &
        fi
    fi
done

echo "---------------------------------------------------------"
echo " All background download threads successfully spawned!"
echo " Monitoring console processes... Do not close the window."
echo "---------------------------------------------------------"

# Wait command blocks the master shell from terminating until all background forks are completed
wait

echo "========================================================="
echo " PARALLEL TRACK BATCH COMPLETED!"
echo " Logs written to: download_*.log"
echo "========================================================="
