import pcl
import open3d as o3d
import numpy as np
import load
import plane_segmentation
import eulcidian_cluster
import manual_registration
import filter_outliers
import measure_cloud
import global_registration
import convert
import resample
import voxel_grid
import time
import uuid

if __name__ =="__main__":
    start_time = ""
    save_path = "./data/active_process/" + start_time
    cloud_path, cloud_format = load.get_file()
    cloud_1 = pcl.load(cloud_path,cloud_format)
    cloud_1_o3d = o3d.io.read_point_cloud(cloud_path)

    cloud_path, cloud_format = load.get_file()
    cloud_2 = pcl.load(cloud_path,cloud_format)
    cloud_2_o3d = o3d.io.read_point_cloud(cloud_path)

    print("Eliminating horizontal planes...")
    no_plane_cloud_1 = plane_segmentation.segment(cloud_1)
    no_plane_cloud_2 = plane_segmentation.segment(cloud_2)

    # print("Saving...")
    # pcl.save(no_plane_cloud_1,(save_path + "/plane_cloud1.ply"), format="ply", binary=True)
    # pcl.save(no_plane_cloud_2,(save_path + "/plane_cloud2.ply"), format="ply", binary=True)
    
    print("Clustering Clouds...")
    cluster_1 = eulcidian_cluster.cluster_and_select(cloud_1_o3d, no_plane_cloud_1)
    cluster_2 = eulcidian_cluster.cluster_and_select(cloud_2_o3d, no_plane_cloud_2)

    # print("Saving...")
    # pcl.save(cluster_1,(save_path + "/cluster_cloud1.ply"), format="ply", binary=True)
    # pcl.save(cluster_2,(save_path + "/cluster_cloud2.ply"), format="ply",binary=True)

    # print("Selecting clusters...")
    # cloud_cluster_1 = o3d.io.read_point_cloud((save_path + "/cluster_cloud1.ply"), cloud_format)
    # cloud_cluster_2 = o3d.io.read_point_cloud((save_path + "/cluster_cloud2.ply"), cloud_format)

    cloud_cluster_1 = convert.pcl_to_o3d(cluster_1)
    cloud_cluster_2 = convert.pcl_to_o3d(cluster_2)


    print("Preparing clusters for registration")
    voxel_size = 0.05 #5cm average
    source, target, source_down, target_down, source_fpfh, target_fpfh = \
        global_registration.prepare_dataset(cloud_cluster_1, cloud_cluster_2,voxel_size)

    print("Calculating Global Registration...")
    globally_registered_cloud = global_registration.execute_global_registration(source_down,target_down,
                                                                                source_fpfh,target_fpfh,
                                                                                voxel_size)
    print("Calculating ICP Registration...")
    result_icp = global_registration.refine_registration(source, target, 
                                                         source_fpfh, target_fpfh,
                                                         globally_registered_cloud.transformation,
                                                         voxel_size)

    print("Transforming Source...")
    cloud_cluster_1.transform(result_icp.transformation)
    regeristered_cloud = cloud_cluster_1 + cloud_cluster_2

    
    
    # o3d.io.write_point_cloud((save_path + "regeristered_cloud.ply"),regeristered_cloud, write_ascii=True, compressed=True)

    if len(regeristered_cloud.points) > 1000:
        regeristered_cloud = convert.o3d_to_pcl(regeristered_cloud)

        pcl.save(regeristered_cloud,(save_path + "regeristered_prefilter_cloud.ply"), format="ply")
        #remove outliers
        regeristered_cloud = filter_outliers.statistical_filter(regeristered_cloud)

        #smooth data
        regeristered_cloud = resample.smooth(regeristered_cloud,0.01)
        
        #average and reduce point size
        regeristered_cloud = voxel_grid.filter(regeristered_cloud,leaf_size=0.005) #0.5cm
        
        print("Saving...")
        pcl.save(regeristered_cloud,(save_path + "regeristered_cloud.ply"), format="ply")
        #convert to o3d to measure
        regeristered_cloud = convert.pcl_to_o3d(regeristered_cloud)


    print("Measuring")
    measure_cloud.manual_measure(regeristered_cloud)


    








    


