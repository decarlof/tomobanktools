#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Functions useful for fly-scan
"""

from __future__ import print_function

import os
import numpy as np
import matplotlib.pyplot as plt

def blur_error(exposure_time, readout_time, camera_size_x, angular_range, number_of_proj):
    """
    Calculate the blur error due to a rotary stage fly scan motion durng the exposure.

    Parameters
    ----------
    exposure_time: float
        Detector exposure time
    readout_time : float
        Detector read out time
    camera_size_x : int
        Detector X size
    angular_range : float
        Tomographic scan angular range
    number_of_proj : int
        Numember of projections

    Returns
    -------
    float
        Blur error in pixel. For good quality reconstruction this should be < 0.2 pixel.
    """

    angular_step = angular_range/number_of_proj
    scan_time = number_of_proj * (exposure_time + readout_time)
    rot_speed = angular_range / scan_time
    frame_rate = number_of_proj / scan_time
    blur_delta = exposure_time * rot_speed
    blur_pixel = (camera_size_x / 2.0) - ((camera_size_x / 2.0) * np.cos(blur_delta * np.pi /180.))

    #print("*************************************")
    #print("Total # of proj: ", number_of_proj)
    #print("Exposure Time: ", exposure_time, "s")
    #print("Readout Time: ", readout_time, "s")
    #print("Angular Range: ", angular_range, "degrees")
    #print("Camera X size: ", camera_size_x)
    #print("*************************************")
    #print("Angular Step: ", angular_step, "degrees")   
    #print("Scan Time: ", scan_time ,"s") 
    #print("Rot Speed: ", rot_speed, "degrees/s")
    #print("Frame Rate: ", frame_rate, "fps")
    #print("Blur: ", blur_pixel, "pixels")
    #print("*************************************")
    
    return blur_pixel, rot_speed, scan_time

def set_acquisition(blur_error, exposure_time, readout_time, camera_size_x, angular_range, number_of_proj):

    """
    Calculate frame rate and rotation speed for a desired blur error t

    Parameters
    ----------
    blur_error : float
        Desired blur error. For good quality reconstruction this should be < 0.2 pixel.
    exposure_time: float
        Detector exposure time
    readout_time : float
        Detector read out time
    camera_size_x : int
        Detector X size
    angular_range : float
        Tomographic scan angular range
    number_of_proj : int
        Numember of projections

    Returns
    -------
    float
        frame_rate, rot_speed
    """

    delta_blur  = np.arccos(((camera_size_x / 2.0) - blur_error) / (camera_size_x / 2.0)) * 180.0 / np.pi
    rot_speed = delta_blur  / exposure_time

    scan_time = angular_range / rot_speed
    frame_rate = number_of_proj / scan_time
    print("*************************************")
    print("Total # of proj: ", number_of_proj)
    print("Exposure Time: ", exposure_time, "s")
    print("Readout Time: ", readout_time, "s")
    print("Angular Range: ", angular_range, "degrees")
    print("Camera X size: ", camera_size_x)
    print("Blur Error: ", blur_error, "pixels")
    print("*************************************")
    print("Rot Speed: : ", rot_speed, "degrees/s")
    print("Scan Time:: ", scan_time, "s")
    print("Frame Rate: ", frame_rate, "fps")
    print("*************************************")
  
    return frame_rate, rot_speed

if __name__ == '__main__':

    exposure_time          = 0.01            # s
    readout_time           = 0.0             # s
    camera_size_x          = 2048            # pixel
    angular_range          = 180.0           # deg
    number_of_proj         = 1500

    x = []    
    y = []
    y1 = []  
    y2 = []  

    for number_of_proj in range(5120, 20480, 64):
        b_err, rot_speed, scan_time = blur_error(exposure_time, readout_time, camera_size_x, angular_range, number_of_proj)
        x.append(number_of_proj)
        y.append(b_err)
        y1.append(rot_speed)
        y2.append(scan_time)
        print(number_of_proj, b_err)
        #print(number_of_proj)
        
        #x.append(number_of_proj)        
        #y.append(b_err)
        #plt.plot([x, y])
    #x = np.arange(0, 5, 0.1);
    #y = np.sin(x)
    plt.plot(x, y)
    #plt.plot(x, y1)
    #plt.plot(x, y2)

    #plt.gca().set_aspect('equal', adjustable='box')
    
    plt.show()

    #blur_error = 0.00143736498376        # pixel
    #frame_rate, rot_speed = set_acquisition(blur_error, exposure_time, readout_time, camera_size_x, angular_range, number_of_proj)
    
    
    
