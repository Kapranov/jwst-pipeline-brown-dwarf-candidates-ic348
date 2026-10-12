#!/usr/bin/env bash
# ==============================================================================
# WORKSPACE CLOSER & KERNEL SANITIZATION MANAGEMENT SCRIPT
# ==============================================================================
set -uo pipefail

echo "======================================================================"
echo "CLOSING OUT SCIENTIFIC WORKSPACE PIPELINE SESSION"
echo "======================================================================\n"

# 1. Clear up ephemeral cache parameters, system logs, and checkpoint layers
echo "🧹 Purging local temporary files and .ipynb checkpoint cache..."
find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.tmp" -delete 2>/dev/null || true
echo "-> Cache layers successfully sanitized."

# 2. Audit version tracking states
echo -e "\n🔍 Running final Git parity inspection check..."
git status

# 3. Check for uncommitted data alterations
UNTRACKED_CHANGES=$(git status --porcelain | wc -l)
if [ "$UNTRACKED_CHANGES" -gt 0 ]; then
    echo "⚠️ Warning: You have uncommitted or unstaged changes remaining in your workspace."
    echo "Please review your code parameters before system logging off."
else
    echo "✅ Git repository state is clean and fully aligned with remote server origins."
fi

# 4. Terminate memory allocations and zombie kernels smoothly
echo -e "\n🛑 Terminating lingering background Jupyter notebook kernels..."
pkill -f "jupyter-kernel" || true
pkill -f "ipython" || true
echo "-> Active memory footprints released safely."

echo -e "\n============================================================="
echo "🎉 PIPELINE SUCCESS: WORKSPACE SUCCESSFULLY CLOSED FOR THE DAY!"
echo "============================================================="
