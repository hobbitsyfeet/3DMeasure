from cloud_compare_icp import per_part_registration
import pca

import load
import open3d as o3d

def normalize_pose(file_list_source, file_list_target):
    pass

if __name__ == "__main__":

    print("Please select a folder with all the parts to normalize")
    file_list_source = load.get_files_from_folder()
    file_list_target = load.get_files_from_folder()
    
    # register each part NOTE: OUTPUT DOES NOT WORK
    per_part_registration(file_list_source, file_list_target, "")

    # generate pca for each part. NOTE: THIS DOES NOT PERFORM ON REGISTERED OBJECTS.
    # this should be a part of per-part registration as the pca can act as a global registration.
    o3d_obj = []
    for file in file_list_source:
        pcd = o3d.io.read_point_cloud(file, format="ply")
        o3d_obj.append(pcd)

        vectors, center, result = pca.get_pca(pcd)
        line_set = pca.o3d_pca_geometry(vectors, center)

        o3d_obj.append(line_set)
    
    # a sphere to 
    mesh_sphere = o3d.create_mesh_sphere()
    mesh_sphere.compute_vertex_normals()
    mesh_sphere.paint_uniform_color([0.1, 0.1, 0.7])
    
    o3d_obj.append(mesh_sphere)

    o3d.draw_geometries(o3d_obj)
    print("Complete")

    