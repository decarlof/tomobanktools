#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to convert the Petra III P05 nanoCT data saved as tiff using the Anka directory structure
"""

from __future__ import print_function

import os
import numpy as np
import tomopy
import dxchange
import dxfile.dxtomo as dx

if __name__ == '__main__':

    # Set tomobank id
    tomobank_id = 'tomo_00077'

    # Set path to the micro-CT data to convert.
    fname = '/Users/decarlo/Desktop/data/scan_renamed_450projections_crop'
    
    # Set meta-data
    experimenter_name="Emanuel Larsson"
    experimenter_affiliation="Helmholtz-Zentrum Geesthacht" 
    experimenter_email="emanuel.larsson@hzg.de"
    instrument_name="nanoCT"  
    source_name="Petra III"  
    source_beamline="P05"  
    sample_name = 'NPG_01'
    detector_name = 'xxxx'
    detector_actual_pixel_size_x = '19.8'
    detector_actual_pixel_size_y = '19.8'
    detector_actual_pixel_size_x_unit = 'nm'
    detector_actual_pixel_size_y_unit = 'nm'
    objective_magnification = 'xxxxx'
    scintillator_name = 'xxxxxx'

    start_date = 'xxxxxxxx'
    end_date = 'xxxxxxxx'
    start_angle = '0'
    start_angle_unit = 'deg'
    end_angle = '180'
    end_angle_unit = 'deg'
    angular_step = '0.4'
    angular_step_unit = 'deg'
    
    proj_start = 0
    proj_end = 451
    flat_start = 0
    flat_end = 93
    dark_start = 0
    dark_end = 10

    ind_tomo = range(proj_start, proj_end)
    ind_flat = range(flat_start, flat_end)
    ind_dark = range(dark_start, dark_end)

    # Select the sinogram range to convert.
    start = 200
    end = 204

    # Read the APS 2-BM raw data.
    #proj, flat, dark = dxchange.read_anka_topotomo(fname, ind_tomo, ind_flat, ind_dark, sino=(start, end))
    proj, flat, dark = dxchange.read_anka_topotomo(fname, ind_tomo, ind_flat, ind_dark)

    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = np.linspace(0, 180, proj.shape[0])
    theta = np.round(theta + 0.005, 2)
       
    print (proj.shape, flat.shape, dark.shape, theta.shape)

    # Convert into a data-exchange file.
    fname = '/Users/decarlo/Desktop/data/' + tomobank_id + '.h5'
    if (fname != None):
        if os.path.isfile(fname):
            print ("Data Exchange file already exists: ", fname)
        else:
            # Create new folder.
            dirPath = os.path.dirname(fname)
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

            # Open DataExchange file
            f = dx.File(fname, mode='w') 

            # Write the Data Exchange HDF5 file.
            f.add_entry(dx.Entry.experimenter(name={'value': experimenter_name}))
            f.add_entry(dx.Entry.experimenter(affiliation={'value': experimenter_affiliation}))
            f.add_entry(dx.Entry.experimenter(email={'value': experimenter_email}))
            f.add_entry(dx.Entry.source(name={'value': source_name}))
            f.add_entry(dx.Entry.source(beamline={'value': source_beamline}))
            f.add_entry(dx.Entry.instrument(name={'value': instrument_name}))
            f.add_entry(dx.Entry.sample(name={'value': sample_name}))
            f.add_entry(dx.Entry.detector(name={'value': detector_name}))
            f.add_entry(dx.Entry.detector(actual_pixel_size_x={'value': detector_actual_pixel_size_x, 'unit': detector_actual_pixel_size_x_unit}))
            f.add_entry(dx.Entry.detector(actual_pixel_size_y={'value': detector_actual_pixel_size_y, 'unit': detector_actual_pixel_size_y_unit}))
            f.add_entry(dx.Entry.objective(magnification={'value': objective_magnification}))
            f.add_entry(dx.Entry.scintillator(name={'value': scintillator_name}))

            f.add_entry(dx.Entry.data(data={'value': proj, 'units':'counts'}))
            f.add_entry(dx.Entry.data(data_white={'value': flat, 'units':'counts'}))
            f.add_entry(dx.Entry.data(data_dark={'value': dark, 'units':'counts'}))
            f.add_entry(dx.Entry.data(theta={'value': theta, 'units':'degrees'}))

            f.add_entry(dx.Entry.acquisition(start_date={'value': start_date}))
            f.add_entry(dx.Entry.acquisition(end_date={'value': end_date}))

            f.add_entry(dx.Entry.acquisition(rotation_start_angle={'value': start_angle, 'unit': start_angle_unit}))
            f.add_entry(dx.Entry.acquisition(rotation_end_angle={'value': end_angle, 'unit': end_angle_unit}))
            f.add_entry(dx.Entry.acquisition(angular_step={'value': angular_step, 'unit': angular_step_unit}))

            f.close()
 
    else:
           print ("Nothing to do ...")

