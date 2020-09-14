import numpy as np
import pcl
import random

from helper.load import get_file

import pcl.pcl_visualization
import pcl


def segment(pcl_cloud):

    ne = pcl_cloud.make_NormalEstimation()
    tree = pcl_cloud.make_kdtree()
    ne.set_SearchMethod(tree)
    ne.set_KSearch(50)


    seg = pcl_cloud.make_segmenter_normals(ksearch=50)
    seg.set_optimize_coefficients(True)
    seg.set_model_type(pcl.SACMODEL_NORMAL_PLANE)
    seg.set_normal_distance_weight(0.1)
    seg.set_method_type(pcl.SAC_RANSAC)
    seg.set_max_iterations(1000)
    seg.set_distance_threshold(0.05)
    # seg.set_InputNormals (cloud_normals)
    [inliers_plane, coefficients_plane] = seg.segment()


    cloud_plane = pcl_cloud.extract(inliers_plane, True)
    return cloud_plane

if __name__ == "__main__":

    cloud_path, cloud_format = get_file()

    # pcl_cloud = pcl.load(cloud_path, cloud_format)
    pcl_cloud = pcl.load(cloud_path, cloud_format)

    viewer = pcl.pcl_visualization.CloudViewing()
    viewer.ShowMonochromeCloud(pcl_cloud)
    pcl_cloud = segment(pcl_cloud)
    # pcl.save(pcl_cloud, "./data/_test_plane_segmentation_skelleton.ply", format="ply")
    pcl.save(pcl_cloud, "./data/_test_plane_segmentation.ply", format="ply")
