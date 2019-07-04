import pcl
from load import get_file

def ply2pcd(cloud_path = None):
    if cloud_path is None:
        cloud_path, cloud_format = get_file()

    cloud = pcl.load(cloud_path, cloud_format)
    cloud_path = cloud_path[:-3]
    print(cloud_path)
    pcl.save_XYZRGBA(cloud, (cloud_path + "pcd"), format="pcd")
    


if __name__ == "__main__":
   ply2pcd()
   
