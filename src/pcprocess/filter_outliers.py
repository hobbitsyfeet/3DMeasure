# Removing outliers using a Conditional or RadiusOutlier removal
# http://pointclouds.org/documentation/tutorials/remove_outliers.php#remove-outliers

import pcl
import numpy as np
import random

import argparse
import load

def stat_filter(pcl_cloud, meank=50, mul_thresh=1.0):
    """
    meank: Set the number of points (k) to use for mean distance estimation.
    mul_thresh: Set the standard deviation multiplier threshold.
            All points who have a distance larger than mul_thresh standard deviation of the mean distance
    """
    sor = pcl_cloud.make_statistical_outlier_filter()
    sor.set_mean_k(meank)
    sor.set_negative(False)
    sor.set_std_dev_mul_thresh(mul_thresh)
    cloud_filtered = sor.filter()
    return cloud_filtered
        # Test
        # cloud_filtered = cloud






if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()', sort='time')
    cloud_path, cloud_format = load.get_file()
    cloud = pcl.load(cloud_path, cloud_format)
    filtered = stat_filter(cloud,cloud.size,0.1)
    viewer = pcl.pcl_visualization.CloudViewing()
    viewer.ShowMonochromeCloud(filtered, b'cloud')
    v = True
    while v:
        v = not(viewer.WasStopped())