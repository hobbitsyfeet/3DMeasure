import pcl
import open3d as o3d
import numpy as numpy
import load
import plane_segmentation
import eulcidian_cluster
import manual_registration
import filter_outliers
import measure_cloud
import global_registration
import resample
import time
import uuid

if __name__ =="__main__":
    start_time = ""
    save_path = "./data/active_process/" + start_time
    cloud_path, cloud_format = load.get_file()
    cloud_1 = pcl.load(cloud_path,cloud_format)

    cloud_path, cloud_format = load.get_file()
    cloud_2 = pcl.load(cloud_path,cloud_format)

    print("Eliminating horizontal planes...")
    no_plane_cloud_1 = plane_segmentation.segment(cloud_1)
    no_plane_cloud_2 = plane_segmentation.segment(cloud_2)

    print("Saving...")
    pcl.save(no_plane_cloud_1,(save_path + "/plane_cloud1.ply"), format="ply", binary=True)
    pcl.save(no_plane_cloud_2,(save_path + "/plane_cloud2.ply"), format="ply", binary=True)
    
    print("Clustering Clouds...")
    cloud_clusters_1 = eulcidian_cluster.cluster(no_plane_cloud_1)
    cloud_clusters_2 = eulcidian_cluster.cluster(no_plane_cloud_2)

    print("Saving...")
    viewer = pcl.pcl_visualization.CloudViewing()
    cluster_number = 0
    for cluster in cloud_clusters_1:
        if cluster.size > 0:
            # cluster = filter_outliers.stat_filter(cluster)
            # cluster = resample.smooth(cluster, 0.01)
            viewer.ShowMonochromeCloud(cluster, uuid.uuid4().bytes)
            cluster_number += 1
            print(cluster_number)
            # time.sleep(1)
            pcl.save(cluster,(save_path + "/"+ str(cluster_number) + "-cluster_cloud1.ply"), format="ply", binary=True)
    cluster_number = 0
    for cluster in cloud_clusters_2:
        if cluster.size > 0:
            # cluster = filter_outliers.stat_filter(cluster)
            # cluster = resample.smooth(cluster, 0.01)
            viewer.ShowMonochromeCloud(cluster, uuid.uuid4().bytes)
            cluster_number += 1
            print(cluster_number)
            # time.sleep(1)
            pcl.save(cluster,(save_path + "/"+ str(cluster_number) + "-cluster_cloud2.ply"), format="ply",binary=True)

    
    
    # PointXYZ
    cloud_path, cloud_format = load.get_file()
    cloud_cluster_1 = o3d.io.read_point_cloud(cloud_path, cloud_format)
    cloud_path, cloud_format = load.get_file()
    cloud_cluster_2 = o3d.io.read_point_cloud(cloud_path, cloud_format)

    voxel_size = 0.05 #5cm average
    source, target, source_down, target_down, source_fpfh, target_fpfh = \
        global_registration.prepare_dataset(cloud_cluster_1, cloud_cluster_2,voxel_size)

    globally_registered_cloud = global_registration.execute_global_registration(source_down,target_down,
                                                                                source_fpfh,target_fpfh,
                                                                                voxel_size)
    
    result_icp = global_registration.refine_registration(source, target, 
                                                         source_fpfh, target_fpfh,
                                                         globally_registered_cloud.transformation,
                                                         voxel_size)

    source.transform(result_icp.transformation)
    regeristered_cloud = source + target
    # registered_cloud = source + target
    # source_aligned, target_aligned = manual_registration.register(cloud_cluster_1, cloud_cluster_2)
    # regeristered_cloud = source_aligned + target_aligned
    o3d.io.write_point_cloud((save_path + "regeristered_cloud.ply"),regeristered_cloud, write_ascii=True)
    # o3d.io.write_point_cloud((save_path + "target_aligned.ply"),target_aligned, write_ascii=True)



    """
    NOTE: need to write conversion function from o3d to pcl at this point.
    Solution is just reading the text, and re-writing double to float, then pcl can load the files.
    OR can change the datatype before it is saved.
    """
    # regeristered_cloud = pcl.load((save_path + "regeristered_cloud.ply"), format="ply")
    # smoothed_merge = resample.smooth(regeristered_cloud, 0.01)

    # pcl.save(smoothed_merge,(save_path + "smoothed_merge.ply"), format="ply")

    # smoothed_merge = o3d.io.read_point_cloud((save_path + "smoothed_merge.ply"), format="ply")

    measure_cloud.manual_measure(regeristered_cloud)


    








    


