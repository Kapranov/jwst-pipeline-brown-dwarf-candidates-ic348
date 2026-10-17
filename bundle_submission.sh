#!/usr/bin/env bash
# ==============================================================================
# 📦 ARCH LINUX AUTOMATED SUBMISSION BUNDLER FOR AAS/ApJ
# Project Core: JWST Multiphase Science Pipeline & Analysis Tracker
# Lead Author: Oleg G.Kapranov
# Date: 15 October 2026
# ==============================================================================

# Explicit color environment indicators
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0;37m'

echo -e "${CYAN}======================================================================${NC}"
echo -e "${CYAN}🚀 STANDARDIZING MANUSCRIPT ASSETS FOR AAS CONTEXT PLATFORM DELIVERY  ${NC}"
echo -e "${CYAN}======================================================================${NC}\n"

# Define destination directory parameters
SUBMIT_DIR="./AAS_Submission_Bundle"
TARGET_TAR="Kapranov_ApJ_JWST_IC348_v1.tar.gz"

# 1. Clear out stale environment configurations
if [ -d "$SUBMIT_DIR" ]; then
    echo -e "${CYAN}[1/5] Removing stale bundle artifacts...${NC}"
    rm -rf "$SUBMIT_DIR"
fi
rm -f "$TARGET_TAR"

# 2. Re-initialize secure extraction layout
echo -e "${CYAN}[2/5] Creating clean deployment tree structures...${NC}"
mkdir -p "$SUBMIT_DIR"

# 3. Synchronize core manuscript files and verification figures
echo -e "${CYAN}[3/5] Moving validated publication coordinates...${NC}"
cp manuscript.tex "$SUBMIT_DIR/"
cp manuscript.pdf "$SUBMIT_DIR/"

# Copy figures exactly matching the integrated LaTeX image calls
cp ./processed_stage3/ic348_substellar_cmd.png "$SUBMIT_DIR/"
cp ./processed_stage3/ic348_halpha_accretion_spatial_map_optimized.png "$SUBMIT_DIR/"
cp ./processed_stage3/ic348_dual_activity_diagnostic_panels.png "$SUBMIT_DIR/"
cp ./processed_stage3/ic348_accretion_vs_extinction_correlation.png "$SUBMIT_DIR/"

# 4. Generate the compressed tarball vector archive
echo -e "${CYAN}[4/5] Executing gzip file compression steps...${NC}"
cd "$SUBMIT_DIR" || exit
tar -czf "../$TARGET_TAR" *
cd ..

# 5. Conduct integrity validation check
echo -e "${CYAN}[5/5] Checking final submission directory parameters...${NC}"
if [ -f "$TARGET_TAR" ]; then
    SIZE_KB=$(du -k "$TARGET_TAR" | cut -f1)
    echo -e "\n${GREEN}======================================================================${NC}"
    echo -e "${GREEN}🎉 SUCCESS: SUBMISSION PACKAGE COMPICATED AND COMPRESSED SUCCESSFULLY!${NC}"
    echo -e "${GREEN}📦 Archive Target Name: $TARGET_TAR ${NC}"
    echo -e "${GREEN}📈 Total Package Weight: ${SIZE_KB} KB ${NC}"
    echo -e "${GREEN}======================================================================${NC}"
else
    echo -e "\n${RED}❌ ERROR: Bundling sequence terminated abruptly. Verify file system links.${NC}"
fi
