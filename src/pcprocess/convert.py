from load import get_file

import pcl
import open3d as o3d
import numpy as np

def ply2pcd(file_path = None):
    if file_path is None:
        file_path, file_format = get_file()

    cloud = pcl.load(file_path, cloud_format)
    file_path = file_path[:-3]
    print(file_path)
    pcl.save_XYZRGBA(cloud, (file_path + "pcd"), format="pcd")
    

def o3d_to_pcl(o3d_cloud):
    """
    Converts open3d pointcloud to pcl pointcloud via numpy.
    """
    # convert Open3D.o3d.geometry.PointCloud to numpy array
    np_cloud = np.asarray(o3d_cloud.points)

    #the most important step, converting double to float. PCL does not support double
    np_cloud = np_cloud.astype('float32')
    
    pcl_cloud = pcl.PointCloud()
    pcl_cloud.from_array(np_cloud)

    return pcl_cloud


def pcl_to_o3d(pcl_cloud):
    """
    Converts pcl pointcloud to open3d pointcloud to via numpy.
    """
    #convert pcl cloud to numpy cloud
    np_cloud = np.empty([pcl_cloud.width, 3], dtype=np.float32)
    np_cloud = np.asarray(pcl_cloud)
    np_cloud = pcl_cloud.to_array()

    #create o3d pointcloud and assign it
    o3d_cloud = o3d.geometry.PointCloud()
    o3d_cloud.points = o3d.utility.Vector3dVector(np_cloud)

    return o3d_cloud
    
def pcl_to_numpy(pcl_cloud):
    """
    Converts pcl pointcloud to numpy array.
    """
    np_cloud = np.empty([pcl_cloud.width, 3], dtype=np.float32)
    np_cloud = np.asarray(pcl_cloud)
    np_cloud = pcl_cloud.to_array()
    return np_cloud

def o3d_to_numpy(o3d_cloud):
    """
    Converts open3d pointcloud to numpy array
    """
    np_cloud = np.asarray(o3d_cloud.points)
    return np_cloud



if __name__ == "__main__":
    # ply2pcd()
    cloud_path, cloud_format = get_file()
    pcl_pointcloud = pcl.load(cloud_path)
    o3d_pointcloud = pcl_to_o3d(pcl_pointcloud)

    print(o3d_pointcloud)

    pcl_pointcloud = o3d_to_pcl(o3d_pointcloud)

    print(pcl_pointcloud)

