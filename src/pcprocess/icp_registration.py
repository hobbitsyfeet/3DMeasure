
# -*- coding: utf-8 -*-
# How to use Normal Distributions Transform
# http://pointclouds.org/documentation/tutorials/normal_distributions_transform.php#normal-distributions-transform

import copy

import numpy as np
import open3d as o3d
import pcl
import pcl.pcl_visualization

from load import get_file

# int main (int argc, char** argv)


# def main():

#     file_path, file_format = get_file()
#     target_cloud = pcl.load(file_path, format=file_format)

#     file_path, file_format = get_file()
#     input_cloud = pcl.load(file_path, format=file_format)

#     print("creating icp")
#     icp = target_cloud.make_IterativeClosestPoint()

#     fitness = 0
#     estimate = input_cloud

#     print("starting icp")
#     converged, transf, estimate, fitness = icp.icp(target_cloud, estimate)
#     print("finished icp")
#     print("converged: " + str(converged))
#     print("translation: " + str(transf))
#     print("estimate: " + str(estimate))
#     print("fitness: " + str(fitness))
            
#     visual = pcl.pcl_visualization.CloudViewing()
    
#     # PointXYZ
#     visual.ShowMonochromeCloud(estimate, b'cloud1')
#     visual.ShowMonochromeCloud(target_cloud, b'cloud2')
#     visual.ShowMonochromeCloud(input_cloud, b'cloud3')


#     v = True
#     while v:
#         v = not(visual.WasStopped())


def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])


if __name__ == "__main__":

    # main()

    source_path, source_format = get_file()
    target_path, target_format = get_file()
    source = o3d.io.read_point_cloud(source_path)
    target = o3d.io.read_point_cloud(target_path)
    threshold = 0.02
    trans_init = np.asarray([[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1 , 0], 
                             [0.0, 0.0, 0.0, 1.0]])
    print("Initial alignment")
    evaluation = o3d.registration.evaluate_registration(source, target,
                                                        threshold, trans_init)
    print(evaluation)

    print("Apply point-to-point ICP")
    reg_p2p = o3d.registration.registration_icp(
        source, target, threshold, trans_init,
        o3d.registration.TransformationEstimationPointToPoint(),
        o3d.registration.ICPConvergenceCriteria(max_iteration = 50000000))
    print(reg_p2p)
    print("Transformation is:")
    print(reg_p2p.transformation)
    print("")
    
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    #source_temp.transform(reg_p2p.transformation)

    draw_registration_result(source, target, reg_p2p.transformation)
    out = target_temp + source_temp
    o3d.io.write_point_cloud("./test_registration.pcd", out)

    draw_registration_result(source, target, reg_p2p.transformation)

