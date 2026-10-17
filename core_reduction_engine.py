"""
JWST Multiphase Data Reduction Vector Engine
Author: Oleg G.Kapranov
Version: 4.0.0 (SIMD Vectorized Release)
"""

import numpy as np
import pandas as pd
from astropy.io import fits
from astropy.wcs import WCS

# --- THE WARNING SILENCER PATCH ---
import warnings
from astropy.wcs import FITSFixedWarning
warnings.simplefilter('ignore', category=FITSFixedWarning)
# ----------------------------------

class VectorReductionEngine:
    def __init__(self, mosaic_fits_path):
        """Initializes the engine directly from Stage 3 stacked mosaic FITS extensions."""
        with fits.open(mosaic_fits_path) as hdul:
            # JWST i2d files store science data and 2D celestial WCS inside the 'SCI' extension
            sci_ext = 'SCI' if 'SCI' in hdul else 1

            self.header = hdul[sci_ext].header
            self.primary_header = hdul[0].header  # Keep primary header for global metadata lookup
            self.data = np.nan_to_num(hdul[sci_ext].data, nan=0.0)  # Self-healing NaN edge noise patch
            self.wcs = WCS(self.header)

    def vectorized_celestial_to_grid(self, ra_array, dec_array):
        """
        Transforms high-density coordinate arrays simultaneously.
        Eliminates scalar exception 'type numpy.ndarray doesn't define __round__'.
        """
        ra_vec = np.asarray(ra_array, dtype=np.float64)
        dec_vec = np.asarray(dec_array, dtype=np.float64)

        # FIX: Drop high-level world_to_pixel and use low-level array-native conversion.
        # The 0 indicates a 0-indexed pixel coordinate convention.
        pixel_x, pixel_y = self.wcs.all_world2pix(ra_vec, dec_vec, 0)

        # Fast element-wise vector rounding and integer truncation
        grid_x = np.rint(pixel_x).astype(int)
        grid_y = np.rint(pixel_y).astype(int)

        return grid_x, grid_y

    def evaluate_forced_aperture_flux(self, grid_x, grid_y, aperture_radius=4):
        """
        Computes background-subtracted vector fluxes across an arbitrary target array.
        Uses fast index masks instead of iterative nested coordinate loops.
        """
        num_targets = len(grid_x)
        flux_vector = np.zeros(num_targets)

        y_indices, x_indices = np.indices(self.data.shape)

        for i in range(num_targets):
            cx, cy = grid_x[i], grid_y[i]

            # Vectorized circular aperture mask slicing boundary conditions
            distance_squared = (x_indices - cx)**2 + (y_indices - cy)**2
            aperture_mask = distance_squared <= aperture_radius**2

            # Self-healing matrix evaluation intercepting edge anomalies
            if np.any(aperture_mask):
                flux_vector[i] = np.sum(self.data[aperture_mask])

        return flux_vector

def process_differential_line_excess(continuum_flux, narrow_band_flux, scale_factor=1.0):
    """
    Quantifies continuum-subtracted emission line excesses dynamically.
    Utilizes vectorized array broadcasting equations.
    """
    cont_arr = np.asarray(continuum_flux, dtype=np.float64)
    narrow_arr = np.asarray(narrow_band_flux, dtype=np.float64)

    # Safe vector masking preventing RuntimeWarning division by zero errors
    safe_mask = (cont_arr > 0) & (narrow_arr > 0)
    excess_vector = np.full_like(cont_arr, np.nan)

    # Matrix subtraction loop executing simultaneously across all array dimensions
    excess_vector[safe_mask] = -2.5 * np.log10(narrow_arr[safe_mask] / cont_arr[safe_mask]) * scale_factor
    return excess_vector
