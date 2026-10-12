#!/usr/bin/env bash
# ==============================================================================
# JWST REPOSITORY AUTOMATED BACKUP ENGINE (ARCH LINUX IMPLEMENTATION)
# ==============================================================================
set -euo pipefail

# 1. Define source and destination path vectors
SOURCE_DIR="/home/kapranov/data_jwst/jwst-pipeline-brown-dwarf-candidates-ic348/processed_stage3"
BACKUP_ROOT="/home/kapranov/data_jwst_backups" # Adjust this path to your external drive mount point
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="${BACKUP_ROOT}/archive_${TIMESTAMP}"
LOG_FILE="${BACKUP_ROOT}/backup_log_${TIMESTAMP}.txt"

echo "======================================================================"
echo "STARTING AUTOMATED JWST STAGE 3 DATASET BACKUP ENGINE"
echo "======================================================================"
echo "Source path:      ${SOURCE_DIR}"
echo "Destination path: ${BACKUP_DIR}"

# 2. Verify source directory existence bounds
if [ ! -d "$SOURCE_DIR" ]; then
    echo "❌ ERROR: Target Stage 3 science folder path does not exist." >&2
    exit 1
fi

# 3. Create target backup workspace structures
mkdir -p "$BACKUP_ROOT"
mkdir -p "$BACKUP_DIR"

echo "Calculating current folder footprint sizes..."
du -sh "$SOURCE_DIR"

# 4. Synchronize data using rsync with delta verification flags
echo "Executing high-speed bitstream data replication loop..."
rsync -av --progress \
    --exclude="*.tmp" \
    --exclude="*chkpnt*" \
    "$SOURCE_DIR/" "$BACKUP_DIR/" 2>&1 | tee "$LOG_FILE"

# 5. Verify sync success criteria
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "\n-------------------------------------------------------------"
    echo "✅ DATASET BACKUP SUCCESSFUL"
    echo "-------------------------------------------------------------"
    echo "Destination archive size footprint:"
    du -sh "$BACKUP_DIR"
    echo "Log report written to: ${LOG_FILE}"
    echo "============================================================="
else
    echo "❌ CRITICAL ERROR: Delta file replication failed or was interrupted." >&2
    exit 2
fi
