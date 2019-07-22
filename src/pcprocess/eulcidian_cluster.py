import copy

import numpy as np
import open3d as o3d
import pcl

import load
#for select_cluster
from o3d_select import pick_points


def euclid_cluster(pcl_cloud):
    """
    PCL_cloud is clustered with a distance threshold of 1cm.
    Clusters smaller than 100 points are removed.
    """
    # pcl_cloud = pcl.load(cloud_path, format=cloud_format)
    
    print(pcl_cloud.size)
    #downsample with a leaf size of 1cm
    vox_grid = pcl_cloud.make_voxel_grid_filter()
    vox_grid.set_leaf_size(0.01, 0.01, 0.01)
    cloud_filtered = vox_grid.filter()

    #create the segmentation for the planar model and set all parameters
    print("Creating Segmentation")
    
    seg = pcl_cloud.make_segmenter()
    seg.set_optimize_coefficients(True)
    seg.set_model_type(pcl.SACMODEL_PLANE)
    #seg.set_model_type(pcl.SAC_RANSAC)
    seg.set_MaxIterations(100)
    seg.set_distance_threshold(0.01)
    print("Starting to Segment")
    indices, model = seg.segment()
    print("Finished Segmenting")


    tree = cloud_filtered.make_kdtree()

    #extract the planar inliers from the input pcl_cloud
    ec = cloud_filtered.make_EuclideanClusterExtraction()
    ec.set_ClusterTolerance(0.02) # 2cm
    ec.set_MinClusterSize(200)
    ec.set_MaxClusterSize(2500000)
    ec.set_SearchMethod(tree)
    cluster_indices = ec.Extract()

    cloud_cluster = pcl.PointCloud()
    cloud_clusters = []
    for j, indices in enumerate(cluster_indices):
        # print("indices = " + str(indices))
        points = np.zeros((len(indices), 3), dtype=np.float32)


        for i, indice in enumerate(indices):
            points[i][0] = cloud_filtered[indice][0]
            points[i][1] = cloud_filtered[indice][1]
            points[i][2] = cloud_filtered[indice][2]

        
        # print("saving")
        cloud_cluster.from_array(points)
        cloud_copy = copy.deepcopy(cloud_cluster)
        cloud_clusters.append(cloud_copy)
        # ss = "cloud_cluster_" + str(j) + ".pcd"
        # pcl.save(cloud_cluster, ss)
    return cloud_clusters

def cluster_and_select(original_o3d_cloud, filtered_pcl_cloud):
    """
    Original_o3d_cloud is the open3d cloud used for only for viewing.
    Filtered_pcl_cloud is the pcl cloud, and can be filtered. As long as the points have not been altered or smoothed.
        Can remove floor, but do not distort the targets.

    """
    #cluster the filtered cloud
    clustered_cloud = euclid_cluster(filtered_pcl_cloud)


    cluster_number = 0
    found = False
    while not found:
        
        #choose point from original cloud, this is to keep the RGB values
        select_point = pick_points(original_o3d_cloud)

        #convert the array to list rounded to the 1 decimal place.
        #1 decimal place has best results for mathcing.
        select_cloud = np.asarray(original_o3d_cloud.points)
        select_point = select_cloud[select_point]
        select_point = [round(x,1) for x in select_point[0]]

        #create list for selected points
        selected_point_coord = []
        selected_point_coord.append(select_point[0])
        selected_point_coord.append(select_point[1])
        selected_point_coord.append(select_point[2])
        print(selected_point_coord)
        # print(len(clustered_cloud))
        #search clusters for the point
        for cluster in clustered_cloud:
            
            np_cloud = np.empty([cluster.width, 3], dtype=np.float32)
            np_cloud = np.asarray(cluster)

            #for each point in cluster, round to the nearest 1 decimal place
            for point in range(len(np_cloud)):
                cluster_coord = [round(x,1) for x in np_cloud[point]]

                #check all three conditions.
                if str(selected_point_coord[0]) == str(cluster_coord[0]):
                    if str(selected_point_coord[1]) == str(cluster_coord[1]):
                        if str(selected_point_coord[2]) == str(cluster_coord[2]):
                            found = True
                            break
            if found is True:
                break
            else:
                cluster_number += 1
        
        if found is False:
            print("Cluster has not been found...")
        
        
    print("Point is in cluster " + str(cluster_number))
    return clustered_cloud[cluster_number]




if __name__ == "__main__":
    cloud_path, cloud_format = load.get_file()
    pcl_original = pcl.load(cloud_path, cloud_format)
    o3d_original = o3d.io.read_point_cloud(cloud_path, cloud_format)
    clusters = cluster_and_select(o3d_original, pcl_original)
    vis = pcl.pcl_visualization.CloudViewing()
    vis.ShowMonochromeCloud(clusters)
    v = True
    while v:
        v = not(vis.WasStopped())

    # cloud_path, cloud_format = load.get_file()
    # cloud = pcl.load(cloud_path, cloud_format)
    # o3d_cloud = o3d.io.read_point_cloud(cloud_path, cloud_format)
    
    # select_point = pick_points(o3d_cloud)

    # select_cloud = np.asarray(o3d_cloud.points)

    # select_point = select_cloud[select_point]
    # select_point = [round(x,2) for x in select_point[0]]

    # selected_point_coord = []
    # selected_point_coord.append(select_point[0])
    # selected_point_coord.append(select_point[1])
    # selected_point_coord.append(select_point[2])
    # print(selected_point_coord)



    # clustered_cloud = cluster(cloud)

    # cluster_number = 0
    # found = False
    # for cluster in clustered_cloud:

    #     np_cloud = np.empty([cluster.width, 3], dtype=np.float32)
    #     np_cloud = np.asarray(cluster)

    #     for point in range(len(np_cloud)):
    #         cluster_coord = [round(x,2) for x in np_cloud[point]]
    #         if str(selected_point_coord[0]) == str(cluster_coord[0]):
    #             print("X MATCHES")
    #             if str(selected_point_coord[1]) == str(cluster_coord[1]):
    #                 print("Y MATCHES")
    #                 if str(selected_point_coord[2]) == str(cluster_coord[2]):
    #                     found = True
    #                     break
    #     if found is True:
    #         break
        
    #     cluster_number += 1
    # print("Point is in cluster " + str(cluster_number))





    # cluster_number = 0
    # selected_cluster = None
    # for indices in enumerate(cluster_indices):
    #     cluster_number += 1
    #     if selected_cluster !- 
    #     for index in indices:
    #         if select_point == index:
    #             selected_cluster = cluster_number
    #             break

    # o3d_cluster_list = []

    # for cluster in clustered_cloud:
    #     cluster_number += 1
    #     save_path = ("./data/_test_euclidean_cluster_"+ str(cluster_number) + ".ply")
    #     print(save_path)
    #     pcl.save(cluster, save_path, format="ply")
    #     o3d_cluster = o3d.io.read_point_cloud(save_path, format="ply")
    #     geometry = copy.deepcopy(o3d_cluster)
    #     o3d_cluster_list.append(geometry)

    # print(o3d_cluster_list)
    # select_cluster(o3d_cluster_list)
    # o3d.visualization.Visualizer()


    # cluster_number = 0
    # for cluster in clouds:
    #     if cluster.size > 0:
    #         # cluster = filter_outliers.stat_filter(cluster)
    #         # cluster = resample.smooth(cluster, 0.01)
    #         # viewer.ShowMonochromeCloud(cluster, uuid.uuid4().bytes)
    #         cluster_number += 1
    #         # print(cluster_number)
    #         # time.sleep(1)
