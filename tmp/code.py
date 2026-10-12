if not os.path.exists(clean_sample_path):
    print(f"ERROR: Clean 205-target sample catalog missing at path: {clean_sample_path}")
else:
    bd_df = pd.read_csv(clean_sample_path)
    print(f"Loaded {len(bd_df)} pristine brown dwarf candidates for multi-band alignment.")

    mosaic_files = glob.glob(os.path.join(stage3_dir, "hh211_stacked_mosaic_*_i2d.fits"))

    if len(mosaic_files) == 0:
        print(f"ERROR: No Stage 3 mosaics (*_i2d.fits) located in {stage3_dir} yet.")
    else:
        print(f"Found {len(mosaic_files)} science-ready multi-filter mosaics for analysis.\n")

        for mosaic_path in mosaic_files:
            base_name = os.path.basename(mosaic_path)
            filter_tag = base_name.replace("hh211_stacked_mosaic_", "").replace("_i2d.fits", "")

            print(f" -> Forced aperture parsing across track filter channel: {filter_tag.upper()}")

            try:
                with fits.open(mosaic_path) as hdul:
                    sci_data = hdul['SCI'].data      
                    sci_header = hdul['SCI'].header  
                    wcs_engine = WCS(sci_header)     

                pixel_x_list, pixel_y_list, flux_val_list = [], [], []

                for _, target in bd_df.iterrows():
                    target_sky = SkyCoord(ra=target['RA_deg'], dec=target['Dec_deg'], unit=u.deg, frame='icrs')
                    pixel_x, pixel_y = wcs_engine.all_world2pix(target_sky.ra.deg, target_sky.dec.deg, 0)
                    x_idx, y_idx = int(round(pixel_x)), int(round(pixel_y))

                    if 0 <= y_idx < sci_data.shape[0] and 0 <= x_idx < sci_data.shape[1]:
                        pixel_flux = sci_data[y_idx, x_idx]
                    else:
                        pixel_flux = np.nan

                    pixel_x_list.append(pixel_x)
                    pixel_y_list.append(pixel_y)
                    flux_val_list.append(pixel_flux)

                bd_df[f'X_{filter_tag}'] = pixel_x_list
                bd_df[f'Y_{filter_tag}'] = pixel_y_list
                bd_df[f'flux_{filter_tag}'] = flux_val_list

            except Exception as e:
                print(f"   -> ERROR processing filter map channel {filter_tag.upper()}: {e}")

        bd_df.to_csv(output_master_catalog, index=False)
        print(f"\nMaster science cross-match table written to: {output_master_catalog}")

Loaded 205 pristine brown dwarf candidates for multi-band alignment.
Found 5 science-ready multi-filter mosaics for analysis.

 -> Forced aperture parsing across track filter channel: F150W2_F164N
   -> ERROR processing filter map channel F150W2_F164N: type numpy.ndarray doesn't define __round__ method
 -> Forced aperture parsing across track filter channel: F150W2_F162M
   -> ERROR processing filter map channel F150W2_F162M: type numpy.ndarray doesn't define __round__ method
 -> Forced aperture parsing across track filter channel: F322W2_F323N
   -> ERROR processing filter map channel F322W2_F323N: type numpy.ndarray doesn't define __round__ method
 -> Forced aperture parsing across track filter channel: F444W_F466N
   -> ERROR processing filter map channel F444W_F466N: type numpy.ndarray doesn't define __round__ method
 -> Forced aperture parsing across track filter channel: F444W_F470N
   -> ERROR processing filter map channel F444W_F470N: type numpy.ndarray doesn't define __round__ method

Master science cross-match table written to: ./processed_stage3/ic348_combined_master_science_catalog.csv

WARNING: FITSFixedWarning: 'datfix' made the change 'Set DATE-BEG to '2022-08-28T12:01:48.011' from MJD-BEG.
Set DATE-AVG to '2022-08-28T12:18:58.815' from MJD-AVG.
Set DATE-END to '2022-08-28T12:36:09.605' from MJD-END'. [astropy.wcs.wcs]
WARNING: FITSFixedWarning: 'obsfix' made the change 'Set OBSGEO-L to   -51.191779 from OBSGEO-[XYZ].
Set OBSGEO-B to   -20.358317 from OBSGEO-[XYZ].
Set OBSGEO-H to 1522868104.452 from OBSGEO-[XYZ]'. [astropy.wcs.wcs]
WARNING: FITSFixedWarning: 'datfix' made the change 'Set DATE-BEG to '2022-08-28T13:16:36.078' from MJD-BEG.
Set DATE-AVG to '2022-08-28T13:21:15.272' from MJD-AVG.
Set DATE-END to '2022-08-28T13:25:54.498' from MJD-END'. [astropy.wcs.wcs]
WARNING: FITSFixedWarning: 'obsfix' made the change 'Set OBSGEO-L to   -51.165411 from OBSGEO-[XYZ].
Set OBSGEO-B to   -20.334369 from OBSGEO-[XYZ].
Set OBSGEO-H to 1522589638.453 from OBSGEO-[XYZ]'. [astropy.wcs.wcs]
WARNING: FITSFixedWarning: 'datfix' made the change 'Set DATE-BEG to '2022-08-28T12:41:53.065' from MJD-BEG.
Set DATE-AVG to '2022-08-28T12:49:24.070' from MJD-AVG.
Set DATE-END to '2022-08-28T12:56:55.044' from MJD-END'. [astropy.wcs.wcs]
WARNING: FITSFixedWarning: 'obsfix' made the change 'Set OBSGEO-L to   -51.184683 from OBSGEO-[XYZ].
Set OBSGEO-B to   -20.351872 from OBSGEO-[XYZ].
Set OBSGEO-H to 1522793138.168 from OBSGEO-[XYZ]'. [astropy.wcs.wcs]
WARNING: FITSFixedWarning: 'datfix' made the change 'Set DATE-BEG to '2022-08-28T12:01:48.011' from MJD-BEG.
Set DATE-AVG to '2022-08-28T12:09:19.009' from MJD-AVG.
Set DATE-END to '2022-08-28T12:16:49.991' from MJD-END'. [astropy.wcs.wcs]
WARNING: FITSFixedWarning: 'obsfix' made the change 'Set OBSGEO-L to   -51.202724 from OBSGEO-[XYZ].
Set OBSGEO-B to   -20.368259 from OBSGEO-[XYZ].
Set OBSGEO-H to 1522983772.441 from OBSGEO-[XYZ]'. [astropy.wcs.wcs]
WARNING: FITSFixedWarning: 'datfix' made the change 'Set DATE-BEG to '2022-08-28T12:21:07.626' from MJD-BEG.
Set DATE-AVG to '2022-08-28T12:28:38.600' from MJD-AVG.
Set DATE-END to '2022-08-28T12:36:09.605' from MJD-END'. [astropy.wcs.wcs]
WARNING: FITSFixedWarning: 'obsfix' made the change 'Set OBSGEO-L to   -51.196440 from OBSGEO-[XYZ].
Set OBSGEO-B to   -20.362552 from OBSGEO-[XYZ].
Set OBSGEO-H to 1522917362.178 from OBSGEO-[XYZ]'. [astropy.wcs.wcs]
