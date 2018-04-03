#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to convert the Elettra data saved as elettra native dxchange (data in sinogram order) in projection ordered dxchange 
"""

from __future__ import print_function

import os
import numpy as np
import tomopy
import dxchange
import dxfile.dxtomo as dx

if __name__ == '__main__':

    # Set tomobank id
    #tomobank_id = 'tomo_00025'
    #sample_name = 'Rock no oil'

    tomobank_id = 'tomo_00026'
    sample_name = 'Rock oil saturated'

    # Set path to the micro-CT data to convert.
    fname = '/local/dataraid/tomobank/' + tomobank_id + '/native/' + tomobank_id + '.h5'
    
    # Set meta-data
    experimenter_name="Lucia Mancini"
    experimenter_affiliation="Elettra Sincrotrone Trieste" 
    experimenter_email="lucia.mancini@elettra.eu"
    instrument_name="Syrmep"  
    source_name="Elettra"  
    source_beamline="Syrmep"  
    detector_name = 'SCMOS 16-bit'
    detector_actual_pixel_size_x = '2.04'
    detector_actual_pixel_size_y = '2.04'
    detector_actual_pixel_size_x_unit = 'microns'
    detector_actual_pixel_size_y_unit = 'microns'
    detector_exposure_time = 0.020
    sample_detector_distance = 150
    source_energy = 2

    start_date = '2011-06-23T18:03:13Z'
    end_date = '2011-06-23T18:27:40Z'
    start_angle = '0'
    start_angle_unit = 'deg'
    end_angle = '180'
    end_angle_unit = 'deg'
    angular_step = '0.45'
    angular_step_unit = 'deg'
    

    # Read the Elettra raw data.
    sino, sflat, sdark, th = dxchange.read_aps_32id(fname)

    proj = np.swapaxes(sino,0,1)
    flat = np.swapaxes(sflat,0,1)
    dark = np.swapaxes(sdark,0,1)

    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = tomopy.angles(proj.shape[0], ang1=0.0, ang2=180.0)

    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = np.linspace(0, 180, proj.shape[0])
    theta = np.round(theta + 0.005, 2)
       
    print (proj.shape, flat.shape, dark.shape, theta.shape)

    # Convert into a data-exchange file.
    fname = '/local/dataraid/tomobank/' + tomobank_id + '/' + tomobank_id + '.h5'
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
            f.add_entry(dx.Entry.detector(exposure_time={'value':detector_exposure_time}))

            f.add_entry(dx.Entry.source(energy={'value':source_energy, 'units':'GeV'}))
            f.add_entry(dx.Entry.sample_stack_setup(detector_distance={'value':sample_detector_distance, 'units':'mm'}))

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

