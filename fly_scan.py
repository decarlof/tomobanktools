#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Check theta generation
"""

from __future__ import print_function

import os
import numpy as np


if __name__ == '__main__':

    exposure_time          = 0.1             # s
    angular_range          = 180.0           # deg
    readout_time           = 0.000           # s
    blur_error             = 0.159            # pixel
    blur_error             = 0.1            # pixel

    camera_size_x          = 2048            # pixel
    number_of_proj         = 180

    min_scan_time = number_of_proj * (exposure_time + readout_time)
    max_rot_speed = angular_range / min_scan_time
    max_frame_rate = number_of_proj / min_scan_time

    max_delta_blur = np.arccos(((camera_size_x/2.0) - blur_error) / (camera_size_x/2.0)) * 180.0 / np.pi
    max_rot_speed_blur = max_delta_blur / exposure_time

    angular_step = angular_range/number_of_proj
 
    blur_delta = exposure_time * max_rot_speed
    blur_pixel = (camera_size_x / 2.0) - ((camera_size_x / 2.0) * np.cos(blur_delta * np.pi /180.))

    min_scan_time_blur = angular_range / max_rot_speed_blur 
#    max_frame_rate_blur = number_of_proj / min_scan_time_blur
    max_frame_rate_blur = number_of_proj / min_scan_time_blur

    print("Exposure Time: ", exposure_time, "s")
    print("Total # of proj: ", number_of_proj)
    print("Angular Range: ", angular_range, "degrees")

    print("Angular Step: ", angular_step, "degrees")   

    print("Max Rot Speed: ", max_rot_speed, "degrees/s")
    print("Min Scan Time: ", min_scan_time ,"s") 
    print("Max Frame Rate: ", max_frame_rate, "fps")

    print("Set Blur Error: ", blur_error, "pixel")
    print("Max Rot Speed before blurring: ", max_rot_speed_blur, "degrees/s")
    print("Min Scan Time before blurring: ", min_scan_time_blur, "s")
    print("Max Frame Rate before blurring: ", max_frame_rate_blur, "fps")

    #print("Blur delta: ", blur_delta)
    #print("Blur pixel: ", blur_pixel)
    #print("Blur delta max: ", max_delta_blur)
 