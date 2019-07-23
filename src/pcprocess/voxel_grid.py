import pcl

def filter(pcl_cloud, leaf_size=0.01):
    sor = pcl_cloud.make_voxel_grid_filter()
    sor.set_leaf_size(0.01, 0.01, 0.01)
    cloud_filtered = sor.filter()
    return cloud_filtered
