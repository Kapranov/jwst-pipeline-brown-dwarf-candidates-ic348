import os
import sys

print("==========================================")
print("RUNNING STEP 2: METADATA SPACE DISCOVERY")
print("==========================================")

# --- NEW: CRITICAL ENVIRONMENT SECURITY CHECK ---
# Check if the MAST token is set in the active terminal space
if "MAST_API_TOKEN" not in os.environ or not os.environ["MAST_API_TOKEN"]:
    print("⚠️  WARNING: No 'MAST_API_TOKEN' detected in environment variables!")
    print(" -> Archive downloads and metadata queries may fail or run slowly.")
    print(" -> To resolve this, run this command in your terminal before running the script:")
    print("    export MAST_API_TOKEN=\"your_actual_token_here\"\n")
    print("------------------------------------------")
else:
    print("✅ Success: 'MAST_API_TOKEN' recognized in workspace environment variables.")
    print("------------------------------------------")

search_scripts = [
    "./search_jw01257-o003_20260714t164831.py",
    "./search_jw01257-o003_20260714t164831_00002.py",
    "./search_jw01257-o003_20260714t164831_00005.py",
    "./search_jw01257-o003_20260714t164831_00007.py",
    "./search_jw01257-o003_20260714t164831_00008.py",
    "./search_jw01257-o003_20260714t164831_00009.py"
]

for script in search_scripts:
    if os.path.exists(script):
        print(f"Executing: {script}")
        try:
            exec(open(script).read(), globals())
            print(f" -> SUCCESS: {script} synchronized cleanly.")
        except Exception as e:
            print(f" -> ERROR executing {script}: {e}")
    else:
        print(f"Skipping (not found): {script}")

print("\nStep 2 Check Complete.")
