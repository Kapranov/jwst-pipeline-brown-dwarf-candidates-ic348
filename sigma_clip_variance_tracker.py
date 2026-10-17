"""
JWST Multiphase Data Reduction: Vectorized Sigma-Clipped Tracker
Author: Oleg G. Kapranov
Version: 4.1.0 (SIMD Variance Release)
"""

import numpy as np

class VectorSigmaClipper:
    def __init__(self, sigma_threshold=3.0, max_iterations=5, convergence_tolerance=0.01):
        """Initializes the statistical tracking variables for the vector matrix."""
        self.sigma = float(sigma_threshold)
        self.max_iter = int(max_iterations)
        self.tol = float(convergence_tolerance)

    def compute_sky_variance_vector(self, data_matrix, grid_x, grid_y, background_annulus_outer=12, background_annulus_inner=6):
        """
        Extracts background annuluses around all coordinate indices simultaneously.
        Applies a vectorized convergence loop to evaluate standard deviations.
        """
        num_targets = len(grid_x)
        sky_variance_vector = np.zeros(num_targets)
        sky_median_vector = np.zeros(num_targets)

        y_indices, x_indices = np.indices(data_matrix.shape)

        for i in range(num_targets):
            cx, cy = grid_x[i], grid_y[i]

            # Vectorized distance mapping for localized background annulus slicing
            distance_squared = (x_indices - cx)**2 + (y_indices - cy)**2
            annulus_mask = (distance_squared <= background_annulus_outer**2) & \
                           (distance_squared > background_annulus_inner**2)

            annulus_pixels = data_matrix[annulus_mask]

            # Intercept edge noise or empty boundary condition anomalies
            if len(annulus_pixels) == 0:
                sky_variance_vector[i] = np.nan
                sky_median_vector[i] = np.nan
                continue

            # Execute the localized vectorized sigma-clipping convergence loop
            med, std = self._execute_vector_clipping_loop(annulus_pixels)
            sky_median_vector[i] = med
            sky_variance_vector[i] = std

        return sky_median_vector, sky_variance_vector

    def _execute_vector_clipping_loop(self, pixel_array):
        """Vectorized statistical outlier clipping routine driving stable array convergence."""
        current_pixels = np.copy(pixel_array)
        prev_std = np.inf

        for _ in range(self.max_iter):
            if len(current_pixels) == 0:
                return 0.0, 0.0

            median = np.median(current_pixels)
            std_dev = np.std(current_pixels)

            # Check for early convergence tolerance thresholds
            if abs(prev_std - std_dev) < self.tol or std_dev == 0:
                break

            prev_std = std_dev

            # Vectorized boolean masking: drops extreme values simultaneously
            clipping_mask = abs(current_pixels - median) <= (self.sigma * std_dev)
            current_pixels = current_pixels[clipping_mask]

        return np.median(current_pixels), np.std(current_pixels)
