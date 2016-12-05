#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to convert the Swiss Light Source TOMCAT tomography data as original tiff.
"""

from __future__ import print_function

import os
import numpy as np
import tomopy
import dxchange
import dxfile.dxtomo as dx

if __name__ == '__main__':

    # Set tomobank id
    tomobank_id = 'tomo_00004'
    sample_name = 'Blakely'

    # Set path to the micro-CT data to convert.
    fname = '/local/decarlo/conda/tomobank/datasets/' + tomobank_id + '/native_raw/' + sample_name + '/' + sample_name
    
    # Set meta-data
    experimenter_name = 'Federica Marone'
    experimenter_affiliation = 'Swiss Light Source' 
    experimenter_email = 'federica.marone@psi.ch'
    instrument_name = 'TOMCAT microCT'  
    source_name = 'SLS'  
    source_beamline = 'TOMCAT'  
    source_current = '401.096'
    source_current_unit = 'mA'
    sample_name = '/sls/X02DA/data/e11218/Data20/disk3/' + sample_name
    detector_name = 'N/A'
    objective_magnification = '10x'
    scintillator_name = 'LAG 20mu'

    detector_exposure_time = '170'
    detector_exposure_time_unit = 'ms'
    monochromator_mono_stripe = 'Ru/C'
    monochromator_energy = '19.260'
    monochromator_energy_unit = 'keV'
    start_date = '2010-11-08T13:51:56Z'
    number_of_projections = '1441'
    number_of_darks = '20'
    number_of_flats = '200'
    sample_in = '0'
    sample_in_unit = 'deg'
    sample_out = '3000'
    sample_out_unit = 'deg'
    start_angle = '0'
    start_angle_unit = 'deg'
    end_angle = '180'
    end_angle_unit = 'deg'
    angular_step = '0.125'
    angular_step_unit = 'deg'
    sample_x = '66.60'
    sample_y = '4382.00'
    sample_z = '5506.00'
    sample_xx = '-810.12'
    sample_zz = '1612.80'

    # Select the sinogram range to convert.
    start = 300
    end = 304

    # Read the SLS TOMCAT raw data.
#    proj, flat, dark = dxchange.read_sls_tomcat(fname, sino=(start, end))
    proj, flat, dark = dxchange.read_sls_tomcat(fname)
  
    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = np.linspace(0, 180, proj.shape[0])
       
    print (proj.shape, flat.shape, dark.shape, theta.shape)

    # Convert into a data-exchange file.
    fname = '/local/decarlo/conda/tomobank/datasets/' + tomobank_id + '/' + tomobank_id + '.h5'
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
            f.add_entry(dx.Entry.source(current={'value': source_current, 'units': source_current_unit}))
            f.add_entry(dx.Entry.instrument(name={'value': instrument_name}))
            f.add_entry(dx.Entry.sample(name={'value': sample_name}))
            f.add_entry(dx.Entry.detector(name={'value': detector_name}))
            f.add_entry(dx.Entry.objective(magnification={'value': objective_magnification}))
            f.add_entry(dx.Entry.scintillator(name={'value': scintillator_name}))

            f.add_entry(dx.Entry.data(data={'value': proj, 'units':'counts'}))
            f.add_entry(dx.Entry.data(data_white={'value': flat, 'units':'counts'}))
            f.add_entry(dx.Entry.data(data_dark={'value': dark, 'units':'counts'}))
            f.add_entry(dx.Entry.data(theta={'value': theta, 'units':'degrees'}))

            f.add_entry(dx.Entry.detector(exposure_time={'value': detector_exposure_time, 'unit': detector_exposure_time_unit}))
            f.add_entry(dx.Entry.monochromator(mono_stripe={'value': monochromator_mono_stripe}))
            f.add_entry(dx.Entry.monochromator(monochromator_energy={'value': monochromator_energy, 'unit': monochromator_energy_unit}))
            
            f.add_entry(dx.Entry.acquisition(start_date={'value': start_date}))
            f.add_entry(dx.Entry.acquisition(number_of_projections={'value': number_of_projections}))
            f.add_entry(dx.Entry.acquisition(number_of_darks={'value': number_of_darks}))
            f.add_entry(dx.Entry.acquisition(number_of_flats={'value': number_of_flats}))
            f.add_entry(dx.Entry.acquisition(sample_in={'value': sample_in, 'unit': sample_in_unit}))
            f.add_entry(dx.Entry.acquisition(sample_out={'value': sample_out, 'unit': sample_out_unit}))
            f.add_entry(dx.Entry.acquisition(rotation_start_angle={'value': start_angle, 'unit': start_angle_unit}))
            f.add_entry(dx.Entry.acquisition(rotation_end_angle={'value': end_angle, 'unit': end_angle_unit}))
            f.add_entry(dx.Entry.acquisition(angular_step={'value': angular_step, 'unit': angular_step_unit}))
            f.add_entry(dx.Entry.setup(sample_x={'value': sample_x}))
            f.add_entry(dx.Entry.setup(sample_y={'value': sample_y}))
            f.add_entry(dx.Entry.setup(sample_z={'value': sample_z}))
            f.add_entry(dx.Entry.setup(sample_xx={'value': sample_xx}))
            f.add_entry(dx.Entry.setup(sample_zz={'value': sample_zz}))

            f.close()
 
    else:
           print ("Nothing to do ...")

