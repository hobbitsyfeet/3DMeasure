import numpy as np
import open3d as o3d
from copy import deepcopy

from cloud_compare_icp import per_part_registration
from helper import load, pca


def get_length(vector):
    # Get the length of a 3D vector
    return (vector[0]**2 + vector[1]**2 + vector[2]**2)**1/2

def elipse_descriptor(radiusx, radiusy, radiusz):
    # Set of all spherical angles:
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)

    # Cartesian coordinates that correspond to the spherical angles:
    # (this is the equation of an ellipsoid):
    x = radiusx * np.outer(np.cos(u), np.sin(v))
    y = radiusy * np.outer(np.sin(u), np.sin(v))
    z = radiusz * np.outer(np.ones_like(u), np.cos(v))
    print("X" + str(x))
    print(x.shape)
    return np.dstack((x,y,z))


def normalize_pose(file_list_source, file_list_target):
    pass

if __name__ == "__main__":

    print("Please select a folder with all the parts to normalize")
    file_list_source , reg_path = load.get_files_from_folder()
    file_list_target, _ = load.get_files_from_folder()
    
    target_list = deepcopy(file_list_target)
    
    # register each part NOTE: OUTPUT DOES NOT WORK
    per_part_registration(file_list_source, file_list_target, "")

    # generate pca for each part. NOTE: THIS DOES NOT PERFORM ON REGISTERED OBJECTS.
    # this should be a part of per-part registration as the pca can act as a global registration.
    o3d_obj = []
    o3d_reg = []
    print("Loading Source Pose...")
    for file in file_list_source:
        pcd = o3d.io.read_point_cloud(file, format="ply")
        o3d_obj.append(pcd)

        vectors, center, result = pca.get_pca(pcd)
        line_set = pca.o3d_pca_geometry(vectors, center)

        o3d_obj.append(line_set)

    print("Loading Target Pose...")

    for file in target_list:
        pcd2 = o3d.io.read_point_cloud(file, format="ply")
        o3d_obj.append(pcd2)
        o3d_reg.append(pcd2)

        vectors2, center2, result2 = pca.get_pca(pcd2)
        line_set2 = pca.o3d_pca_geometry(vectors2, center2)
        o3d_reg.append(line_set2)
        o3d_obj.append(line_set2)
    
    print("Loading Registration Pose...")
    registered_file_list, _ = load.get_files_from_folder(reg_path ,keyword="REGISTERED")
    for file in registered_file_list:
        pcd3 = o3d.io.read_point_cloud(file, format="ply")
        o3d_reg.append(pcd3)

        vectors3, center3, result3 = pca.get_pca(pcd3)
        line_set3 = pca.o3d_pca_geometry(vectors3, center3)

        o3d_reg.append(line_set3)

    # for file in file_list_target:
    #     pcd = o3d.io.read_point_cloud(file, format="ply")
    #     o3d_obj.append(pcd)

    #     vectors, center, result = pca.get_pca(pcd)
    #     line_set = pca.o3d_pca_geometry(vectors, center)

    #     o3d_obj.append(line_set)
        # print(vectors)
        # elipse = elipse_descriptor(get_length(vectors[0]), get_length(vectors[1]), get_length(vectors[2]))
        
        # print("Elipse Shape" + str(elipse.shape))
        # print(elipse)

        # elipse_cloud = o3d.geometry.PointCloud()
        # elipse_cloud.points = o3d.utility.Vector3dVector(elipse)
        # o3d_obj.append(elipse_cloud)
    # a sphere to 
    # mesh_sphere = o3d.create_mesh_sphere()
    # mesh_sphere.compute_vertex_normals()
    # mesh_sphere.paint_uniform_color([0.1, 0.1, 0.7])


    
    # o3d_obj.append(mesh_sphere)

    o3d.draw_geometries(o3d_obj)
    o3d.draw_geometries(o3d_reg)
    print("Complete")
