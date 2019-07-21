import pcl
import open3d as o3d
import numpy as numpy
import load
import plane_segmentation
import eulcidian_cluster
import manual_registration
import filter_outliers
import measure_cloud
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
        cluster = filter_outliers.stat_filter(cluster)
        viewer.ShowMonochromeCloud(cluster, uuid.uuid4().bytes)
        cluster_number += 1
        print(cluster_number)
        time.sleep(1)
        pcl.save(cluster,(save_path + "/"+ str(cluster_number) + "-cluster_cloud1.ply"), format="ply", binary=True)
    cluster_number = 0
    for cluster in cloud_clusters_2:
        cluster = filter_outliers.stat_filter(cluster)
        viewer.ShowMonochromeCloud(cluster, uuid.uuid4().bytes)
        cluster_number += 1
        print(cluster_number)
        time.sleep(1)
        pcl.save(cluster,(save_path + "/"+ str(cluster_number) + "-cluster_cloud2.ply"), format="ply",binary=True)

    
    
    # PointXYZ
    cloud_path, cloud_format = load.get_file()
    cloud_cluster_1 = o3d.io.read_point_cloud(cloud_path, cloud_format)
    cloud_path, cloud_format = load.get_file()
    cloud_cluster_2 = o3d.io.read_point_cloud(cloud_path, cloud_format)

    registered_cloud = manual_registration.register(cloud_cluster_1, cloud_cluster_2)
    o3d.io.write_point_cloud((save_path + "registered.ply"),registered_cloud)
    measure_cloud.manual_measure(registered_cloud)


    








    


