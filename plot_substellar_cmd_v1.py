import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

stage3_dir = "./processed_stage3/"
master_catalog_path = os.path.join(stage3_dir, "ic348_combined_master_science_catalog.csv")

if not os.path.exists(master_catalog_path):
    print("ERROR: Master combined catalog not found yet. Ensure the extraction script is complete.")
else:
    # 1. Load your master multi-band database
    df = pd.read_csv(master_catalog_path)

    # 2. Standard Astronomical Flux to AB Magnitude Conversion
    # AB_mag = -2.5 * log10(flux) + zeropoint (JWST calibration outputs flux natively)
    # If your pipeline has already mapped magnitudes, substitute the raw columns directly:
    df['mag_F150W2'] = -2.5 * np.log10(df['flux_f150w2_f162m'].clip(lower=1e-5)) + 21.1
    df['mag_F444W'] = -2.5 * np.log10(df['flux_f444w_f470n'].clip(lower=1e-5)) + 21.1

    # Compute the Color Index axis metric
    df['color_150_444'] = df['mag_F150W2'] - df['mag_F444W']

    # 3. Build the Color-Magnitude Diagram
    fig, ax = plt.subplots(figsize=(9, 7))

    # Plot all candidates as high-contrast scientific points
    sc = ax.scatter(df['color_150_444'], df['aper30_abmag'],
                    c=df['mass_M_jup'], cmap='plasma', s=35, edgecolor='black', alpha=0.85)

    cb = plt.colorbar(sc, ax=ax)
    cb.set_label(r"Estimated Mass (Jupiter Masses, $M_J$)", fontsize=11)

    # Standard CMD Orientations (Fainter values go down, Redder values go right)
    ax.invert_yaxis()

    ax.set_title("IC 348 Survey Core: Multi-Filter Color-Magnitude Diagram", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel(r"Color Index: $[F150W2] - [F444W]$ (AB Mag)", fontsize=11)
    ax.set_ylabel(r"Apparent Brightness: $F444W$ (AB Mag)", fontsize=11)

    ax.grid(True, linestyle=':', alpha=0.5)

    output_cmd_path = os.path.join(stage3_dir, "ic348_substellar_cmd_v2.png")
    plt.savefig(output_cmd_path, bbox_inches='tight', dpi=300)
    plt.close(fig)

    print(f"\n==========================================")
    print("COLOR-MAGNITUDE DIAGRAM SUCCESSFULLY EXPORTED!")
    print(f"Saved to: {output_cmd_path}")
    print(f"==========================================")
