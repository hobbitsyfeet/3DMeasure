import pcl
import numpy as np
import uuid
from random import randrange
from pcl import pcl_visualization
from load import get_file
from time import sleep
def reg_grow_segment(cloud,smoothness, view=True):
    

    tree = cloud.make_kdtree()
    #normal estimation
    ne = cloud.make_NormalEstimation()
    ne.set_SearchMethod(tree)
    ne.set_KSearch(50)
    
    print("Creating Region Growing...", end="")
    reg = cloud.make_RegionGrowing(ksearch=50)
    reg.set_MinClusterSize(100)
    reg.set_MaxClusterSize(1000000)
    reg.set_SearchMethod(tree)
    reg.set_NumberOfNeighbours(200)

    print(smoothness/100)
    reg.set_SmoothnessThreshold((smoothness/10)/ 180 * np.pi)
    reg.set_CurvatureThreshold(3.0)
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
            points[i][0] = cloud[indice][0]
            points[i][1] = cloud[indice][1]
            points[i][2] = cloud[indice][2]

        cloud_cluster.from_array(points)
        
        accumulate_clouds.append(cloud_cluster)
        if view is False:
            continue
        else:
            print(">>Finished cluster " + str(j), end='\r', flush=True)
            
            cloud_id = uuid.uuid4().bytes
            # print(cloud_id)
            pccolor = pcl.pcl_visualization.PointCloudColorHandleringCustom(cloud, randrange(0, 255, 1),
                                                                                    randrange(0, 255, 1),
                                                                                    randrange(0, 255, 1))

            viewer.AddPointCloud_ColorHandler(cloud_cluster, pccolor, cloud_id, 0)

            viewer.SpinOnce()
    print("")
    print("Done.")


    # while view:
    #     viewer.Spin()
    #     view = not(viewer.WasStopped())

    return accumulate_clouds
        



if __name__ == "__main__":
    
    cloud_path, cloud_format = get_file()
    cloud = pcl.load(cloud_path, cloud_format)
    for i in range(400):
        clusters = reg_grow_segment(cloud,i,view=True)