
import numpy as np
import pcl
import random

from load import get_file

import pcl.pcl_visualization


def plane_segment(cloud):

    ne = cloud.make_NormalEstimation()
    tree = cloud.make_kdtree()
    ne.set_SearchMethod(tree)
    ne.set_KSearch(50)


    seg = cloud.make_segmenter_normals(ksearch=50)
    seg.set_optimize_coefficients(True)
    seg.set_model_type(pcl.SACMODEL_NORMAL_PLANE)
    seg.set_normal_distance_weight(0.1)
    seg.set_method_type(pcl.SAC_RANSAC)
    seg.set_max_iterations(100)
    seg.set_distance_threshold(0.03)
    # seg.set_InputNormals (cloud_normals)
    [inliers_plane, coefficients_plane] = seg.segment()


    cloud_plane = cloud.extract(inliers_plane, True)
    return cloud_plane

if __name__ == "__main__":
    
    cloud_path, cloud_format = get_file()
    cloud = pcl.load(cloud_path, cloud_format)
    cloud = plane_segment(cloud)
