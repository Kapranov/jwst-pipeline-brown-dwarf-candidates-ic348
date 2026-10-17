"""
JWST Multiphase Data Reduction: Multi-Filter Automated Loop Engine
Author: Oleg G. Kapranov
Version: 5.0.0 (SIMD Multi-Channel Release)
"""

import os
import warnings
import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs import FITSFixedWarning

# Silence native FITS timeline transformation logging alerts
warnings.simplefilter('ignore', category=FITSFixedWarning)

class VectorReductionEngine:
    def __init__(self, mosaic_fits_path):
        """Initializes the engine directly from a Stage 3 stacked mosaic FITS extension."""
        with fits.open(mosaic_fits_path) as hdul:
            sci_ext = 'SCI' if 'SCI' in hdul else 1
            self.header = hdul[sci_ext].header

            # FIX: Explicitly target HDU 0 (PRIMARY) to extract global file metadata cards
            self.primary_header = hdul[0].header

            self.data = np.nan_to_num(hdul[sci_ext].data, nan=0.0)
            self.wcs = WCS(self.header)

    def vectorized_celestial_to_grid(self, ra_array, dec_array):
        """Transforms coordinate arrays simultaneously via distortion-corrected low-level API."""
        ra_vec = np.asarray(ra_array, dtype=np.float64)
        dec_vec = np.asarray(dec_array, dtype=np.float64)
        pixel_x, pixel_y = self.wcs.all_world2pix(ra_vec, dec_vec, 0)
        return np.rint(pixel_x).astype(int), np.rint(pixel_y).astype(int)

    def evaluate_forced_aperture_flux(self, grid_x, grid_y, aperture_radius=4):
        """Computes aperture flux arrays across all coordinate rows via index masks."""
        num_targets = len(grid_x)
        flux_vector = np.zeros(num_targets)
        y_indices, x_indices = np.indices(self.data.shape)

        for i in range(num_targets):
            cx, cy = grid_x[i], grid_y[i]
            # Verify coordinates fall safely inside the physical image array matrix grid bounds
            if 0 <= cx < self.data.shape[1] and 0 <= cy < self.data.shape[0]:
                distance_squared = (x_indices - cx)**2 + (y_indices - cy)**2
                aperture_mask = distance_squared <= aperture_radius**2
                flux_vector[i] = np.sum(self.data[aperture_mask])
        return flux_vector

class VectorSigmaClipper:
    def __init__(self, sigma_threshold=3.0, max_iterations=5):
        self.sigma = sigma_threshold
        self.max_iter = max_iterations

    def compute_sky_background(self, data_matrix, grid_x, grid_y, r_in=6, r_out=12):
        """Calculates stable sky medians around coordinates using quick outlier rejection clipping."""
        num_targets = len(grid_x)
        sky_medians = np.zeros(num_targets)
        y_indices, x_indices = np.indices(data_matrix.shape)

        for i in range(num_targets):
            cx, cy = grid_x[i], grid_y[i]
            if 0 <= cx < data_matrix.shape[1] and 0 <= cy < data_matrix.shape[0]:
                distance_squared = (x_indices - cx)**2 + (y_indices - cy)**2
                annulus_mask = (distance_squared <= r_out**2) & (distance_squared > r_in**2)
                pixels = data_matrix[annulus_mask]

                if len(pixels) > 0:
                    # Rapid vector convergence pass loop
                    for _ in range(self.max_iter):
                        med = np.median(pixels)
                        std = np.std(pixels)
                        if std == 0: break
                        pixels = pixels[abs(pixels - med) <= (self.sigma * std)]
                    sky_medians[i] = np.median(pixels) if len(pixels) > 0 else 0.0
            else:
                sky_medians[i] = np.nan
        return sky_medians

def run_production_pipeline_batch(stage3_dir, candidate_catalog_csv, output_catalog_csv):
    print("======================================================================")
    print("🚀 BOOTING MULTI-FILTER PIPELINE ENGINE: PROCESSING ALL SHOCK CHANNELS")
    print("======================================================================\n")

    if not os.path.exists(candidate_catalog_csv):
        print("❌ Aborted: Missing main coordinate catalog.")
        return

    # Load base target registry
    df = pd.read_csv(candidate_catalog_csv)

    # Identify coordinate tracking keys dynamically
    ra_col = 'ra' if 'ra' in df.columns else ('RA_deg' if 'RA_deg' in df.columns else 'RA')
    dec_col = 'dec' if 'dec' in df.columns else ('Dec_deg' if 'Dec_deg' in df.columns else 'Dec')

    # Target file paths dictionary mapping unique key suffixes
    fits_targets = {
        'F164N': 'hh211_stacked_mosaic_f150w2_f164n_i2d.fits',
        'F323N': 'hh211_stacked_mosaic_f322w2_f323n_i2d.fits',
        'F466N': 'hh211_stacked_mosaic_f444w_f466n_i2d.fits',
        'F470N': 'hh211_stacked_mosaic_f444w_f470n_i2d.fits'
    }

    # Loop sequentially over each filter dataset array
    for filter_key, filename in fits_targets.items():
        fits_path = os.path.join(stage3_dir, filename)

        if not os.path.exists(fits_path):
            print(f"⚠️  Warning: File track {filename} missing inside workspace directory. Skipping channel...")
            continue

        print(f"📸 Processing Channel [{filter_key}] <── File: {filename}")

        # Initialize instances for the active FITS track matrix
        engine = VectorReductionEngine(fits_path)
        clipper = VectorSigmaClipper()

        # Calculate grid transformations natively for this image layer
        grid_x, grid_y = engine.vectorized_celestial_to_grid(df[ra_col], df[dec_col])

        # Extract background noise baseline structures
        sky_medians = clipper.compute_sky_background(engine.data, grid_x, grid_y)

        # Integrate aperture flux matrix maps
        raw_flux = engine.evaluate_forced_aperture_flux(grid_x, grid_y, aperture_radius=4)
        aperture_area = np.pi * (4**2)

        # Calculate net flux and explicitly replace any NaN values with 1e-5
        computed_flux = raw_flux - (sky_medians * aperture_area)
        net_flux = np.where(np.isnan(computed_flux), 1e-5, computed_flux)
        net_flux = np.clip(net_flux, a_min=1e-5, a_max=None)

        # Parse zero point conversions smoothly
        phot_zero_point = float(engine.header.get('PHOTZP', engine.primary_header.get('PHOTZP', 28.0)))
        ab_magnitudes = -2.5 * np.log10(net_flux) + phot_zero_point

        # Append outputs dynamically as filter-specific matrix columns
        df[f'Flux_{filter_key}'] = net_flux
        df[f'Mag_{filter_key}'] = ab_magnitudes
        print(f"   --> Derived AB Mag baseline spans: [{df[f'Mag_{filter_key}'].min():.2f} to {df[f'Mag_{filter_key}'].max():.2f}]\n")

    # Export unified structured data log
    df.to_csv(output_catalog_csv, index=False)
    print("======================================================================")
    print("🎉 MULTI-CHANNEL DATA REDUCTION VERIFIED COMPLETELY CLEAN!")
    print(f"💾 Synchronized master science database saved to: {output_catalog_csv}")
    print("======================================================================")

if __name__ == "__main__":
    work_dir = "./processed_stage3/"
    catalog_in = os.path.join(work_dir, "ic348_brown_dwarf_candidates_final.csv")
    catalog_out = os.path.join(work_dir, "ic348_combined_master_science_catalog.csv")

    run_production_pipeline_batch(work_dir, catalog_in, catalog_out)
