import pcl
import numpy as np
from load import get_file

if __name__ == "__main__":
    cloud_path, cloud_format = get_file()
    cloud = pcl.load(cloud_path, format=cloud_format)
    
    print(cloud.size)
    #downsample with a leaf size of 1cm
    vox_grid = cloud.make_voxel_grid_filter()
    vox_grid.set_leaf_size(0.01, 0.01, 0.01)
    cloud_filtered = vox_grid.filter()

    #create the segmentation for the planar model and set all parameters
    print("Creating Segmentation")
    
    seg = cloud.make_segmenter()
    seg.set_optimize_coefficients(True)
    seg.set_model_type(pcl.SACMODEL_PLANE)
    seg.set_model_type(pcl.SAC_RANSAC)
    seg.set_MaxIterations(100)
    seg.set_distance_threshold(0.02)
    print("Starting to Segment")
    indices, model = seg.segment()
    print("Finished Segmenting")


    tree = cloud_filtered.make_kdtree()

    #extract the planar inliers from the input cloud
    ec = cloud_filtered.make_EuclideanClusterExtraction()
    ec.set_ClusterTolerance(0.02) # 2cm
    ec.set_MinClusterSize(100)
    ec.set_MaxClusterSize(250000)
    ec.set_SearchMethod(tree)
    cluster_indices = ec.Extract()

    cloud_cluster = pcl.PointCloud()

    for j, indices in enumerate(cluster_indices):
        print("indices = " + str(indices))
        points = np.zeros((len(indices), 3), dtype=np.float32)


        for i, indice in enumerate(indices):
            points[i][0] = cloud_filtered[indice][0]
            points[i][1] = cloud_filtered[indice][1]
            points[i][2] = cloud_filtered[indice][2]

        
        print("saving")
        cloud_cluster.from_array(points)
        ss = "cloud_cluster_" + str(j) + ".pcd"
        pcl.save(cloud_cluster, ss)
    
    