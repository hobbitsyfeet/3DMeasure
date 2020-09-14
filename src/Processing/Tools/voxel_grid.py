import pcl
import load
def filter(pcl_cloud, leaf_size=0.01):
    sor = pcl_cloud.make_voxel_grid_filter()
    sor.set_leaf_size(leaf_size, leaf_size, leaf_size)
    cloud_filtered = sor.filter()
    return cloud_filtered

if __name__ == "__main__":
    cp, cf = load.get_file()
    cloud = pcl.load(cp,cf)
    cloud_filtered = filter(cloud, 0.001)
    pcl.save(cloud_filtered, "./data/tests/_test_voxel_grid2.ply")