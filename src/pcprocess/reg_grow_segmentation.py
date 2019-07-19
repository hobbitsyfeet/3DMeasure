import pcl
import numpy as np
import uuid
from random import randrange
from pcl import pcl_visualization
from load import get_file
def reg_grow_segment(cloud, view=True):
    

    tree = cloud.make_kdtree()
    #normal estimation
    ne = cloud.make_NormalEstimation()
    ne.set_SearchMethod(tree)
    ne.set_KSearch(50)
    
    print("Creating Region Growing...", end="")
    reg = cloud.make_RegionGrowing(ksearch=50)
    reg.set_MinClusterSize(20)
    reg.set_MaxClusterSize(1000000)
    reg.set_SearchMethod(tree)
    reg.set_NumberOfNeighbours(200)

    reg.set_SmoothnessThreshold(2.75/ 180 * np.pi)
    reg.set_CurvatureThreshold(120)
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
    while view:
        viewer.Spin()
        view = not(viewer.WasStopped())

    return accumulate_clouds
        



if __name__ == "__main__":
    
    cloud_path, cloud_format = get_file()
    cloud = pcl.load(cloud_path, cloud_format)
    clusters = reg_grow_segment(cloud,view=True)