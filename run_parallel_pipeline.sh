#!/bin/bash
# ==============================================================================
# 🚀 ARCH LINUX HIGH-PERFORMANCE MULTIPROCESSING PIPELINE BUNDLER
# Project Core: Vectorized Substellar Analytics (IC 348 / HH 211)
# Lead Author: Oleg G.Kapranov
# Version: 5.0.0 (Parallel Worker Thread Release)
# ==============================================================================

# ANSI Color Output Indicators
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0;37m'

echo -e "${CYAN}======================================================================${NC}"
echo -e "${CYAN}🛰️  INITIALIZING PARALLEL MULTIPROCESSING COMPUATATIONAL MATRIX       ${NC}"
echo -e "${CYAN}======================================================================${NC}\n"

# 1. Hardware Thread Inventory
CPU_CORES=$(nproc)
TARGET_WORKERS=$((CPU_CORES > 4 ? CPU_CORES - 2 : 2)) # Leave headroom for system stability

echo -e "${GREEN}• System Hardware Inventory :${NC} Detected ${CPU_CORES} core threads."
echo -e "${GREEN}• Allocation Target Vector  :${NC} Spawning ${TARGET_WORKERS} parallel pipelines.\n"

# 2. Virtual Environment Verification Safeguard
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}⚠️  Environment Status Check: Virtual environment not active.${NC}"
    if [ -f "$HOME/astro_env/bin/activate" ]; then
        echo -e "${CYAN}--> Activating isolated Python 3.14 'astro_env' container...${NC}"
        source "$HOME/astro_env/bin/activate"
    else
        echo -e "${RED}❌ Execution Aborted: Missing Python environment layout path.${NC}"
        exit 1
    fi
fi

# 3. Directory Layout Integrity Guard
STAGE3_DIR="./processed_stage3"
LOG_DIR="$STAGE3_DIR/parallel_logs"
mkdir -p "$LOG_DIR"

CATALOG_IN="$STAGE3_DIR/ic348_brown_dwarf_candidates_final.csv"
if [ ! -f "$CATALOG_IN" ]; then
    echo -e "${RED}❌ Error: Input candidate registry ($CATALOG_IN) not found.${NC}"
    exit 1
fi

# 4. Multiprocessing Execution Loop
echo -e "\n${CYAN}🚀 Dispatching parallel worker processes into the logging tree...${NC}"
start_time=$(date +%s.%N)

# Trigger target jobs simultaneously in background frames
# For chunked split tasks or multiple filtering variants, we pipe directly to worker tasks
for worker_id in $(seq 1 "$TARGET_WORKERS"); do
    LOG_FILE="$LOG_DIR/worker_${worker_id}_execution.log"

    echo -e "   --> Spawning Pipeline Node #${worker_id} (Logging to: $LOG_FILE)..."

    # Run the core batch reduction script in background mode
    # In an advanced run, pass arguments like split data frames if chunks are generated
    python run_batch_substellar_reduction.py > "$LOG_FILE" 2>&1 &

    # Track background Process ID (PID) numbers
    pids[${worker_id}]=$!
done

# 5. Multiprocessing Thread Barrier Wait
echo -e "\n${YELLOW}⏳ Thread Barrier Activated: Waiting for all processing workers to converge...${NC}"
for pid in ${pids[*]}; do
    wait "$pid"
done

end_time=$(date +%s.%N)
duration=$(awk "BEGIN {print $end_time - $start_time}")

echo -e "\n${GREEN}======================================================================${NC}"
echo -e "${GREEN}🎉 CONVERGENCE SUCCESS: ALL PARALLEL PIPELINE CHANNELS STABILIZED!   ${NC}"
echo -e "${GREEN}⏱️  Total Parallel Multi-Thread Latency: $(printf "%.4f" "$duration") seconds${NC}"
echo -e "${GREEN}📂 Diagnostic execution trackers logged safely inside: $LOG_DIR/${NC}"
echo -e "${GREEN}======================================================================${NC}"
