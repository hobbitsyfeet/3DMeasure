# examples/Python/Advanced/global_registration.py

import open3d as o3d
import copy
from load import get_file


def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    print("Transforming")
    source_temp.transform(transformation)
    print("Finished Transforming")
    o3d.visualization.draw_geometries([source_temp, target_temp])


def preprocess_point_cloud(o3d_cloud, voxel_size):
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    #pcd_down = pcd.voxel_down_sample(voxel_size)
    
    pcd_down = o3d.geometry.voxel_down_sample(o3d_cloud, voxel_size)

    radius_normal = voxel_size * 2
    print(":: Estimate normal with search radius %.3f." % radius_normal)

    pcd_down_normals = o3d.geometry.estimate_normals(o3d_cloud, o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.registration.compute_fpfh_feature(o3d_cloud, o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    print(pcd_fpfh)
    return o3d_cloud, pcd_fpfh


def prepare_dataset(o3d_source_cloud, o3d_target_cloud, voxel_size=0.01):
    print(":: Load two point clouds and disturb initial pose.")
    # source_path, source_format = get_file()
    # target_path, target_format = get_file()
    # source = o3d.io.read_point_cloud(source_path, format=source_format)
    # target = o3d.io.read_point_cloud(target_path, format=target_format)

    source_down, source_fpfh = preprocess_point_cloud(o3d_source_cloud, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(o3d_target_cloud, voxel_size)
    return o3d_source_cloud, o3d_target_cloud, source_down, target_down, source_fpfh, target_fpfh

def execute_fast_global_registration(source_down, target_down, source_fpfh,
                                     target_fpfh, voxel_size):
    distance_threshold = voxel_size * 0.5
    print(":: Apply fast global registration with distance threshold %.3f" \
            % distance_threshold)
    result = o3d.registration.registration_fast_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh,
        o3d.registration.FastGlobalRegistrationOption(
            maximum_correspondence_distance=distance_threshold))
    return result

def execute_global_registration(source_down, target_down, source_fpfh,
                                target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    print(":: RANSAC registration on downsampled point clouds.")
    print("   Since the downsampling voxel size is %.3f," % voxel_size)
    print("   we use a liberal distance threshold %.3f." % distance_threshold)
    
    result = o3d.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, distance_threshold,
        o3d.registration.TransformationEstimationPointToPoint(True), 4, [
            o3d.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            o3d.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold)
        ], o3d.registration.RANSACConvergenceCriteria(4000000, 200))

    print(result)
    print(result.transformation)
    return result


def refine_registration(source, target, source_fpfh, target_fpfh,ransac_transform, voxel_size):
    distance_threshold = voxel_size * 0.4
    print(":: Point-to-plane ICP registration is applied on original point")
    print("   clouds to refine the alignment. This time we use a strict")
    print("   distance threshold %.3f." % distance_threshold)
    result = o3d.registration.registration_icp(
        source, target, distance_threshold, ransac_transform,
        o3d.registration.TransformationEstimationPointToPoint())
    print(result)
    print(result.transformation)
    return result



# if __name__ == "__main__":
    # voxel_size = 0.05  # means 5cm for the dataset
    # source, target, source_down, target_down, source_fpfh, target_fpfh = \
    #         prepare_dataset(voxel_size)

    # # result_ransac = execute_global_registration(source_down, target_down,
    # #                                             source_fpfh, target_fpfh,
    # #                                             voxel_size)
    # result_ransac = execute_fast_global_registration(source_down, target_down,
    #                                                 source_fpfh, target_fpfh,
    #                                                 voxel_size)

    # draw_registration_result(source_down, target_down,
    #                          result_ransac.transformation)

    # result_icp = refine_registration(source, target, source_fpfh, target_fpfh,
    #                                  voxel_size)

    # draw_registration_result(source, target, result_icp.transformation)

    #out = target_down + source_temp
    #o3d.io.write_point_cloud("./test_registration.pcd", out)