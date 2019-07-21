# Open3D: www.open3d.org
# The MIT License (MIT)
# See license file or visit www.open3d.org for details

# examples/Python/Advanced/interactive_visualization.py

import numpy as np
import copy

import open3d as o3d
import pyrealsense2 as rs2

from load import get_file
from measure_cloud import manual_measure


def demo_crop_geometry():
    print("Demo for manual geometry cropping")
    print(
        "1) Press 'Y' twice to align geometry with negative direction of y-axis"
    )
    print("2) Press 'K' to lock screen and to switch to selection mode")
    print("3) Drag for rectangle selection,")
    print("   or use ctrl + left click for polygon selection")
    print("4) Press 'C' to get a selected geometry and to save it")
    print("5) Press 'F' to switch to freeview mode")
    source_path, source_format = get_file()
    pcd = o3d.io.read_point_cloud(source_path)
    o3d.visualization.draw_geometries_with_editing([pcd])


def read_intrinsics(file_path):
    intrinsics = rs2.intrinsics()
     
    intrinsics_file = open(file_path, "r")
    intr_string = intrinsics_file.read()

    #extract values from file
    
    intr_value = intr_string[intr_string.find("width:"):]
    intrinsics.width = int(intr_value[intr_value.find(":") + 2 :intr_value.find(",")])

    intr_value = intr_string[intr_string.find("height:"):]
    intrinsics.height = int(intr_value[intr_value.find(":") + 2 :intr_value.find(",")])

        
    intr_value = intr_string[intr_string.find("ppx:"):]
    intrinsics.ppx = float(intr_value[intr_value.find(":") + 2 :intr_value.find(",")])

        
    intr_value = intr_string[intr_string.find("ppy:"):]
    intrinsics.ppy = float(intr_value[intr_value.find(":") + 2 :intr_value.find(",")])

        
    intr_value = intr_string[intr_string.find("fx:"):]
    intrinsics.fx = float(intr_value[intr_value.find(":") + 2 :intr_value.find(",")])
    
        
    intr_value = intr_string[intr_string.find("fy:"):]
    intrinsics.fy = float(intr_value[intr_value.find(":") + 2 :intr_value.find(",")])

        
    intr_value = intr_string[intr_string.find("model:"):]
    intr_model = intr_value[intr_value.find(":") + 2 :intr_value.find(",")]
    if intr_model == "None":
        pass
    if intr_model == "Brown Conrady":
        intrinsics.model = rs2.distortion.brown_conrady
    elif intr_model == "Modified Brown Conrady":
        intrinsics.model = rs2.distortion.modified_brown_conrady
    elif intr_model == "Inverse Brown Conrady":
        intrinsics.model = rs2.distortion.inverse_brown_conrady
        

        
    intr_value = intr_string[intr_string.find("coeffs:"):]
    intr_value = intr_value[intr_value.find("[") + 1 : intr_value.find("]")]
    count = sum(chars.count(",") for chars in intr_value)
    intr_coeff = []
    for i in range(5):
        if intr_value.find(",") is not -1:
            print(i)
            print(intr_value)
            intr_coeff.append(float(intr_value[:intr_value.find(",")]))
            intr_value = intr_value[intr_value.find(",") + 2:]
        else:
            intr_coeff.append(float(intr_value))
    print(intr_coeff)
    intrinsics.coeffs = intr_coeff

    return intrinsics


def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    # source_temp.paint_uniform_color([1, 0.706, 0])
    # target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])


def pick_points(pcd):
    print("")
    print(
        "1) Please pick at least three correspondences using [shift + left click]"
    )
    print("   Press [shift + right click] to undo point picking")
    print("2) Afther picking points, press q for close the window")
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.run()  # user picks points
    vis.destroy_window()
    print("")
    #returns the inices of the users picked points
    return vis.get_picked_points()


def register(o3d_source_cloud, o3d_target_cloud):
    print("Demo for manual ICP")
    # source_path, source_format = get_file()
    # target_path, source_format = get_file()
    print("Visualization of two point clouds before manual alignment")
    draw_registration_result(o3d_source_cloud, o3d_target_cloud, np.identity(4))

    # pick points from two point clouds and builds correspondences
    picked_id_source = pick_points(o3d_source_cloud)
    picked_id_target = pick_points(o3d_target_cloud)
    print(picked_id_source)
    assert (len(picked_id_source) >= 3 and len(picked_id_target) >= 3)
    assert (len(picked_id_source) == len(picked_id_target))
    corr = np.zeros((len(picked_id_source), 2))
    corr[:, 0] = picked_id_source
    corr[:, 1] = picked_id_target

    # estimate rough transformation using correspondences
    print("Compute a rough transform using the correspondences given by user")
    p2p = o3d.registration.TransformationEstimationPointToPoint()
    trans_init = p2p.compute_transformation(o3d_source_cloud, o3d_target_cloud,
                                            o3d.utility.Vector2iVector(corr))

    # point-to-point ICP for refinement
    print("Perform point-to-point ICP refinement")
    threshold = 0.03  # 3cm distance threshold
    reg_p2p = o3d.registration.registration_icp(
        o3d_source_cloud, o3d_target_cloud, threshold, trans_init,
        o3d.registration.TransformationEstimationPointToPoint())
    draw_registration_result(o3d_source_cloud, o3d_target_cloud, reg_p2p.transformation)
    source_temp = copy.deepcopy(o3d_source_cloud)
    target_temp = copy.deepcopy(o3d_target_cloud)
    # source_temp.paint_uniform_color([1, 0.706, 0])
    # target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(reg_p2p.transformation)
    # registered_cloud = source_temp + target_temp

    
    return source_temp, target_temp



if __name__ == "__main__":
    cloud_path, cloud_format = get_file()
    cloud_1 = o3d.io.read_point_cloud(cloud_path,cloud_format)
    cloud_path, cloud_format = get_file()
    cloud_2 = o3d.io.read_point_cloud(cloud_path,cloud_format)
    registered_cloud = register(cloud_1,cloud_2)

    o3d.io.write_point_cloud("./data/_test_manualregist.ply",registered_cloud,True)
    #demo_crop_geometry()
    # demo_manual_registration()
    # cloud_path, cloud_format = get_file()
    # cloud = o3d.io.read_point_cloud(cloud_path, format=cloud_format)
    #intrinsics = read_intrinsics((cloud_path[:-4] + "_intrinsics.txt"))
    # length = manual_measure(cloud)
    # distance, segments = measure(cloud)
    #print(segments)