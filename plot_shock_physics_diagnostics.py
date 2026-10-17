"""
JWST Multiphase Data Reduction: Matplotlib Shock Physics Scatter Visualizer
Author: Oleg G. Kapranov
Version: 6.1.0 (SIMD Physics Plotting Release)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_shock_physics_plots(physics_csv_path, output_image_path):
    print("======================================================================")
    print("📊 INITIALIZING MATPLOTLIB DIAGNOSTICS: SHOCK FRONTS SCATTER PLOTS")
    print("======================================================================\n")

    if not os.path.exists(physics_csv_path):
        print("❌ Aborted: Physics-calibrated catalog file not located.")
        return

    # 1. Load the database table
    df = pd.read_csv(physics_csv_path)

    # 2. Dynamic column extraction for mass parameters matching your database
    mass_col = 'mass_M_jup' if 'mass_M_jup' in df.columns else ('Target_Mass' if 'Target_Mass' in df.columns else 'mass')
    if mass_col not in df.columns:
        # Fallback assignment to prevent NameError exceptions if named differently
        print(f"⚠️  Warning: Mass column missing. Available fields: {list(df.columns)}")
        return

    # 3. Clean up the rows using raw Pandas 3.0 dropna selectors
    clean_df = df.dropna(subset=[mass_col, 'Ratio_FeII_H2', 'Estimated_Temp_K'])
    print(f"📈 Slicing finite arrays: Plotting {len(clean_df)} / {len(df)} target nodes.")

    # 4. Initialize a clean 1x2 dual-panel dashboard layout configuration
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), sharex=False)

    # Global title layout definition using raw string formatting to protect text metrics
    fig.suptitle(r"Substellar Shock Dynamics: Derived Gas Properties Across the Mass Function",
                 fontsize=13, fontweight='bold', y=0.98)

    # --- PANEL A: GAS VELOCITY SHOCK MECHANICS ([Fe II] / H2 Line Ratios) ---
    scatter1 = ax1.scatter(clean_df[mass_col], clean_df['Ratio_FeII_H2'],
                          c=clean_df['Estimated_Temp_K'], cmap='plasma',
                          edgecolor='black', alpha=0.8, s=50)

    ax1.set_title(r"Gas Dissociation State: Atomic $[\mathrm{Fe\ II}]$ / Molecular $\mathrm{H}_2$",
                  fontsize=11, fontweight='bold')
    ax1.set_xlabel(r"Estimated Target Mass ($M_{\mathrm{J}}$)", fontsize=10)
    ax1.set_ylabel(r"Line Ratio: Flux $F_{\mathrm{F164N}}$ / Flux $F_{\mathrm{F323N}}$", fontsize=10)
    ax1.grid(True, linestyle=':', alpha=0.5)

    # Structural threshold lines highlighting dissociative J-shocks boundary boundaries
    ax1.axhline(y=1.5, color='crimson', linestyle='--', alpha=0.7, label='Dissociative Shock Ceiling (>1.5)')
    ax1.legend(loc='upper right', fontsize=9)

    # --- PANEL B: SEMI-EMPIRICAL BOLTZMANN GAS TEMPERATURE ESTIMATION ---
    scatter2 = ax2.scatter(clean_df[mass_col], clean_df['Estimated_Temp_K'],
                          c=clean_df['Ratio_FeII_H2'], cmap='viridis',
                          edgecolor='black', alpha=0.8, s=50)

    ax2.set_title(r"Kinematic Thermal Footprint: Semi-Empirical Gas Temperature",
                  fontsize=11, fontweight='bold')
    ax2.set_xlabel(r"Estimated Target Mass ($M_{\mathrm{J}}$)", fontsize=10)
    ax2.set_ylabel(r"Derived Gas Temperature ($T_{\mathrm{gas}}$, Kelvin)", fontsize=10)
    ax2.grid(True, linestyle=':', alpha=0.5)

    # Colorbar vector layouts configurations
    cbar1 = fig.colorbar(scatter1, ax=ax1, pad=0.02)
    cbar1.set_label(r"Estimated Gas Temperature ($T_{\mathrm{gas}}$, K)", fontsize=9)

    cbar2 = fig.colorbar(scatter2, ax=ax2, pad=0.02)
    cbar2.set_label(r"Dissociation Ratio ($F_{\mathrm{F164N}} / F_{\mathrm{F323N}}$)", fontsize=9)

    plt.tight_layout()

    # Save the vector graphics plot clean to disk
    plt.savefig(output_image_path, dpi=250, bbox_inches='tight')
    print(f"🎉 SUCCESS: Publication-grade dashboard exported to: {output_image_path}")
    print("======================================================================")
    plt.show()

if __name__ == "__main__":
    stage3_dir = "./processed_stage3/"
    csv_input = os.path.join(stage3_dir, "ic348_shock_physics_diagnostics.csv")
    png_output = os.path.join(stage3_dir, "ic348_substellar_shock_physics_dashboard.png")

    generate_shock_physics_plots(csv_input, png_output)

