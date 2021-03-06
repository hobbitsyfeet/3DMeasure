import pcl
import numpy as np
import uuid
from random import randrange
from pcl import pcl_visualization
from helper.load import get_file
from time import sleep
from copy import deepcopy
import os
def segment(pcl_cloud, smoothness, curve_thresh=1.0, ksearch=50, 
            neighbours=200, min_cluster=50, max_cluster=100000, 
            view=True):
    """
    Takes a PCL Pointcloud and segments it with region growing segmentation. 
    """
    tree = pcl_cloud.make_kdtree()
    #normal estimation
    ne = pcl_cloud.make_NormalEstimation()
    ne.set_SearchMethod(tree)
    ne.set_KSearch(50)
    
    print("Creating Region Growing...", end="")
    reg = pcl_cloud.make_RegionGrowing(ksearch=ksearch)
    reg.set_MinClusterSize(min_cluster)
    reg.set_MaxClusterSize(max_cluster)
    reg.set_SearchMethod(tree)
    reg.set_NumberOfNeighbours(neighbours)

    reg.set_SmoothnessThreshold(smoothness/ 180 * np.pi)
    reg.set_CurvatureThreshold(curve_thresh)
    cluster_indices = reg.Extract()
    print("Done.")
    cloud_cluster = pcl.PointCloud()

    accumulate_clouds = []

    if view is True:
        viewer = pcl.pcl_visualization.PCLVisualizering()
    print("Generating clusters...")
    for j, indices in enumerate(cluster_indices):
        # print("indices = " + str(indices))
        points = np.zeros((len(indices), 3), dtype=np.float32)


        for i, indice in enumerate(indices):
            points[i][0] = pcl_cloud[indice][0]
            points[i][1] = pcl_cloud[indice][1]
            points[i][2] = pcl_cloud[indice][2]

        cloud_cluster.from_array(points)
        copy = deepcopy(cloud_cluster)
        accumulate_clouds.append(copy)
        if view is False:
            continue
        else:
            print(">>Finished cluster " + str(j), end='\r', flush=True)
            
            cloud_id = uuid.uuid4().bytes
            # print(cloud_id)
            pccolor = pcl.pcl_visualization.PointCloudColorHandleringCustom(pcl_cloud, randrange(0, 255, 1),
                                                                                    randrange(0, 255, 1),
                                                                                    randrange(0, 255, 1))

            viewer.AddPointCloud_ColorHandler(cloud_cluster, pccolor, cloud_id, 0)

            viewer.SpinOnce()
    print("")
    print("Done.")


    while view:
        viewer.Spin()
        view = not(viewer.WasStopped())

    return accumulate_clouds
        



if __name__ == "__main__":

    while(True):
        cloud_path, cloud_format = get_file()

    # for path in cloud_path:

        folder_name = cloud_path[-13:-4]
        cluster_index = 0
        cluster_name = str(cluster_index)[-4:]
        print("Cluster_" + str(cluster_index)[-4:] + "." + cloud_format)
        pcl_cloud = pcl.load(cloud_path, cloud_format)
        # for i in range(400):
        clusters = segment(pcl_cloud,2.75, min_cluster=5, view=False)
        
        for cluster in clusters:
            
            # pcl.save(cluster, ("./data/PRICT-28/clusters/Cluster_" + str(cluster_index)[-4:] + "." + cloud_format), 
            #         format=cloud_format)
            try:
                os.mkdir("F:/Data/Raccoon/Clean/Clustered/Right/81661206"+folder_name)
            except:
                pass
            pcl.save(cluster, ("F:/Data/Raccoon/Clean/Clustered/Right/81661206"+folder_name+"/Cluster_" + str(cluster_index)[-4:] + "." + cloud_format), 
                    format=cloud_format)
            print("Saving ", end="")
            print("Cluster_" + str(cluster_index)[-4:] + "." + cloud_format)
            cluster_index += 1
