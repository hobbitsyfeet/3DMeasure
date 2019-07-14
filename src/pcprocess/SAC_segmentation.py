# -*- coding: utf-8 -*-
from __future__ import print_function

# This Code Base
# http://ros-robot.blogspot.jp/2011/08/pclapi-point-cloud-library-pcl-pcl-api.html

import numpy as np
import pcl
import random

from load import get_file

import pcl.pcl_visualization


def main():
    # pcl::PointCloud<pcl::PointXYZRGB> cloud;
    cloud_path , cloud_format = get_file()
    cloud = pcl.load_XYZRGB(cloud_path, cloud_format)


    # Create the segmentation object
    # pcl::SACSegmentation<pcl::PointXYZRGB> seg
    seg = cloud.make_segmenter()
    # Optional
    seg.set_optimize_coefficients(True)
    # Mandatory
    seg.set_model_type(pcl.SACMODEL_PLANE)
    seg.set_method_type(pcl.SAC_RANSAC)
    seg.set_distance_threshold(0.1)

    # pcl::ModelCoefficients::Ptr coefficients (new pcl::ModelCoefficients)
    # pcl::PointIndices::Ptr inliers (new pcl::PointIndices);
    inliers, model = seg.segment()

    cloud2 = pcl.PointCloud(inliers)
    #
    # pcl::visualization::CloudViewer viewer("Cloud Viewer");
    # viewer.showCloud(cloud.makeShared());
    # while (!viewer.wasStopped ())
    #isual = pcl.pcl_visualization.CloudViewing()
    visual.ShowColorCloud(cloud2)

    print ("test")
    v = True
    while v:
        v = not(visual.WasStopped())


if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()', sort='time')
    main()