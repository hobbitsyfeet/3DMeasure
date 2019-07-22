
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


def main():
    # // Loading first scan of room.
    # pcl::PointCloud<pcl::PointXYZ>::Ptr target_cloud (new pcl::PointCloud<pcl::PointXYZ>);
    # if (pcl::io::loadPCDFile<pcl::PointXYZ> ("room_scan1.pcd", *target_cloud) == -1)
    # {
    # PCL_ERROR ("Couldn't read file room_scan1.pcd \n");
    # return (-1);
    # }
    # std::cout << "Loaded " << target_cloud->size () << " data points from room_scan1.pcd" << std::endl;
    file_path, file_format = get_file()
    target_cloud = pcl.load(file_path, format=file_format)
    # centred = cloud - np.mean(cloud, 0)
    # # print(centred)
    # ptcloud_centred = pcl.PointCloud()
    # ptcloud_centred.from_array(centred)

    # // Loading second scan of room from new perspective.
    # pcl::PointCloud<pcl::PointXYZ>::Ptr input_cloud (new pcl::PointCloud<pcl::PointXYZ>);
    # if (pcl::io::loadPCDFile<pcl::PointXYZ> ("room_scan2.pcd", *input_cloud) == -1)
    # {
    # PCL_ERROR ("Couldn't read file room_scan2.pcd \n");
    # return (-1);
    # }
    # std::cout << "Loaded " << input_cloud->size () << " data points from room_scan2.pcd" << std::endl;
    file_path, file_format = get_file()
    input_cloud = pcl.load(file_path, format=file_format)

    # // Filtering input scan to roughly 10% of original size to increase speed of registration.
    # pcl::PointCloud<pcl::PointXYZ>::Ptr filtered_cloud (new pcl::PointCloud<pcl::PointXYZ>);
    # pcl::ApproximateVoxelGrid<pcl::PointXYZ> approximate_voxel_filter;
    # approximate_voxel_filter.setLeafSize (0.2, 0.2, 0.2);
    # approximate_voxel_filter.setInputCloud (input_cloud);
    # approximate_voxel_filter.filter (*filtered_cloud);
    # std::cout << "Filtered cloud contains " << filtered_cloud->size () << " data points from room_scan2.pcd" << std::endl;
    ##
    print("creating icp")
    icp = target_cloud.make_IterativeClosestPoint()

    # Final = icp.align()
    fitness = 0
    estimate = input_cloud

    print("starting icp")
    converged, transf, estimate, fitness = icp.icp(target_cloud, estimate)
    print("finished icp")
    print("converged: " + str(converged))
    print("translation: " + str(transf))
    print("estimate: " + str(estimate))
    print("fitness: " + str(fitness))
            
    visual = pcl.pcl_visualization.CloudViewing()
    
    # PointXYZ
    visual.ShowMonochromeCloud(estimate, b'cloud1')
    visual.ShowMonochromeCloud(target_cloud, b'cloud2')
    visual.ShowMonochromeCloud(input_cloud, b'cloud3')


    v = True
    while v:
        v = not(visual.WasStopped())
    # pcl version 1.7.2
    # // Initializing Normal Distributions Transform (NDT).
    # pcl::NormalDistributionsTransform<pcl::PointXYZ, pcl::PointXYZ> ndt;
    #
    # // Setting scale dependent NDT parameters
    # // Setting minimum transformation difference for termination condition.
    # ndt.setTransformationEpsilon (0.01);
    # // Setting maximum step size for More-Thuente line search.
    # ndt.setStepSize (0.1);
    # //Setting Resolution of NDT grid structure (VoxelGridCovariance).
    # ndt.setResolution (1.0);
    #
    # // Setting max number of registration iterations.
    # ndt.setMaximumIterations (35);
    #
    # // Setting point cloud to be aligned.
    # ndt.setInputSource (filtered_cloud);
    # Setting point cloud to be aligned to.
    # ndt.setInputTarget (target_cloud);
    ##

    # Set initial alignment estimate found using robot odometry.
    # Eigen::AngleAxisf init_rotation (0.6931, Eigen::Vector3f::UnitZ ());
    # Eigen::Translation3f init_translation (1.79387, 0.720047, 0);
    # Eigen::Matrix4f init_guess = (init_translation * init_rotation).matrix ();
    ##

    # Calculating required rigid transform to align the input cloud to the target cloud.
    # pcl::PointCloud<pcl::PointXYZ>::Ptr output_cloud (new pcl::PointCloud<pcl::PointXYZ>);
    # ndt.align (*output_cloud, init_guess);
    ##

    # std::cout << "Normal Distributions Transform has converged:" << ndt.hasConverged () << " score: " << ndt.getFitnessScore () << std::endl;
    ##

    # // Transforming unfiltered, input cloud using found transform.
    # pcl::transformPointCloud (*input_cloud, *output_cloud, ndt.getFinalTransformation ());
    ##

    # // Saving transformed input cloud.
    # pcl::io::savePCDFileASCII ("room_scan2_transformed.pcd", *output_cloud);
    ##

    # // Initializing point cloud visualizer
    # boost::shared_ptr<pcl::visualization::PCLVisualizer>
    # viewer_final (new pcl::visualization::PCLVisualizer ("3D Viewer"));
    # viewer_final->setBackgroundColor (0, 0, 0);
    ##

    # // Coloring and visualizing target cloud (red).
    # pcl::visualization::PointCloudColorHandlerCustom<pcl::PointXYZ>
    # target_color (target_cloud, 255, 0, 0);
    # viewer_final->addPointCloud<pcl::PointXYZ> (target_cloud, target_color, "target cloud");
    # viewer_final->setPointCloudRenderingProperties (pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 1, "target cloud");
    ##

    # // Coloring and visualizing transformed input cloud (green).
    # pcl::visualization::PointCloudColorHandlerCustom<pcl::PointXYZ>
    # output_color (output_cloud, 0, 255, 0);
    # viewer_final->addPointCloud<pcl::PointXYZ> (output_cloud, output_color, "output cloud");
    # viewer_final->setPointCloudRenderingProperties (pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 1, "output cloud");
    ##

    # // Starting visualizer
    # viewer_final->addCoordinateSystem (1.0, "global");
    # viewer_final->initCameraParameters ();
    ##

    # // Wait until visualizer window is closed.
    # while (!viewer_final->wasStopped ())
    # {
    # viewer_final->spinOnce (100);
    # boost::this_thread::sleep (boost::posix_time::microseconds (100000));
    # }
# examples/Python/Basic/icp_registration.py



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

    # print("Apply point-to-plane ICP")
    # reg_p2l = o3d.registration.registration_icp(
    #     source, target, threshold, trans_init,
    #     o3d.registration.TransformationEstimationPointToPlane())
    # print(reg_p2l)
    # print("Transformation is:")
    # print(reg_p2l.transformation)
    # print("")
    # draw_registration_result(source, target, reg_p2l.transformation)



# if __name__ == "__main__":
#     # import cProfile
#     # cProfile.run('main()', sort='time')
#     main()
