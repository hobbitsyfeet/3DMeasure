# examples/Python/Advanced/non_blocking_visualization.py

import copy

import matplotlib.pyplot as plt
import numpy as np
import open3d as o3d
import pandas as pd
import pcl
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA

from helper import convert
#This downsamples and calculates surface normals
from global_registration import (execute_global_registration,
                                 preprocess_point_cloud)
from helper import load


def get_pca(o3d_cloud):
    pca = PCA(n_components=3)
    df = pd.DataFrame(convert.o3d_to_numpy(o3d_cloud))
    pca.fit(df)
    result = pd.DataFrame(pca.transform(df), columns=['PCA%i' % i for i in range(3)], index=df.index)

    # Plot initialisation
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(result['PCA0'], result['PCA1'], result['PCA2'], cmap="Set2_r", s=60)
    
    # make simple, bare axis lines through space:
    xAxisLine = ((min(result['PCA0']), max(result['PCA0'])), (0, 0), (0,0))
    ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r')
    yAxisLine = ((0, 0), (min(result['PCA1']), max(result['PCA1'])), (0,0))
    ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r')
    zAxisLine = ((0, 0), (0,0), (min(result['PCA2']), max(result['PCA2'])))
    ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'r')
    
    # label the axes
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("")
    
    # plt.show(block=True)
    return (xAxisLine[0],yAxisLine[1],zAxisLine[2])



if __name__ == "__main__":

    source_dir, f1 = load.get_file()
    target_dir, f2 = load.get_file()

    print(source_dir)

    o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)
    source_raw = o3d.io.read_point_cloud(source_dir, format = f1)
    target_raw = o3d.io.read_point_cloud(target_dir, format = f2)

    # source = o3d.geometry.voxel_down_sample(source_raw, voxel_size=0.02)
    # target = o3d.geometry.voxel_down_sample(target_raw ,voxel_size=0.02)
    source, source_fpfh = preprocess_point_cloud(source_raw, voxel_size=0.1)
    target, target_fpfh = preprocess_point_cloud(target_raw, voxel_size=0.1)
    
    result = execute_global_registration(source, target, source_fpfh, target_fpfh, voxel_size=0.1)

    (sx,sy,sz) = get_pca(source)
    (tx,ty,tz) = get_pca(target)
    source.transform(result.transformation)

    # flip_transform = [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]
    # source.transform(flip_transform)
    # target.transform(flip_transform)

    vis = o3d.visualization.Visualizer()
    # pca_lines = [[0,1], 
    #              [2,3], 
    #              [4,5]] 
    # print(sx)
    # source_pca_points = [[sx[0], 0, 0]
    #                     [sx[0], 0, 0]
    #                      [sy[0], sy[1],
    #                      [sz[0], sz[1]]
    # colors = [[1, 0, 0] for i in range(len(pca_lines))]
    # line_set = o3d.geometry.LineSet(
    #     points=o3d.utility.Vector3dVector(source_pca_points),
    #     lines=o3d.utility.Vector2iVector(pca_lines),
    # )
    # line_set.colors = o3d.utility.Vector3dVector(colors)
    vis.create_window()
    # vis.add_geometry([line_set])
    vis.add_geometry(source)
    # vis.add_geometry()
    vis.add_geometry(target)
    threshold = 0.00000001
    icp_iteration = 10000
    save_image = False

    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)

    best_fittness = 0
    evaluate = o3d.registration.evaluate_registration(source, target,3)

    # result = execute_global_registration(source, target, source_fpfh, target_fpfh, voxel_size=0.1/icp_iteration)


    corr = np.zeros((6, 2))
    corr[:, 0] = [(sx[0],0,0), (sx[1],0,0), (0,sy[0],0), sy[1], sz[0], sz[1]]
    corr[:, 1] = [tx[0], tx[1], ty[0], ty[1], tz[0], tz[1]]

    print(corr)

    # estimate rough transformation using correspondences
    print("Compute a rough transform using the correspondences given by user")
    p2p = o3d.registration.TransformationEstimationPointToPoint()
    trans_init = p2p.compute_transformation(source, target,
                                            o3d.utility.Vector2iVector(corr))

    
    
    print("Perform point-to-point ICP refinement")
    threshold = 0.0001  # 3cm distance threshold
    reg_p2p = o3d.registration.registration_icp(
        source, target, threshold, trans_init,
        o3d.registration.TransformationEstimationPointToPoint())
    
    source_temp.transform(reg_p2p.transformation)
    # draw_registration_result(source, target, reg_p2p.transformation)

    # for i in range(icp_iteration):
    #     # result = execute_global_registration(source, target, source_fpfh, target_fpfh, voxel_size=0.1/icp_iteration)

    #     result_icp = o3d.registration.registration_colored_icp(
    #                 source, target, 0.001, np.identity(4),
    #                 o3d.registration.ICPConvergenceCriteria(relative_fitness=1e-6,
    #                                                         relative_rmse=1e-6,
    #                                                         max_iteration=50))

    #     reg_p2p = o3d.registration.registration_icp(
    #         source, target, threshold, np.identity(4),
    #         o3d.registration.TransformationEstimationPointToPoint())

    #     # print(reg_p2p[0])
    #     # source_temp.transform(result.transformation)
        
    #     source_temp.transform(result_icp.transformation)
    #     source_temp.transform(reg_p2p.transformation)
    #     evaluate = o3d.registration.evaluate_registration(source_temp, target,3)

    #     if evaluate.fitness > best_fittness:
    #         # source.transform(result.transformation)
    #         source.transform(reg_p2p.transformation)
    #         source.transform(result_icp.transformation)
    #         evaluate = o3d.registration.evaluate_registration(source, target,3)
    #         best_fittness = evaluate.fitness 
    #     print("EVAL", evaluate.fitness)
    #     print(evaluate)

    while(True):
        vis.update_geometry()
        vis.poll_events()
        vis.update_renderer()
    vis.update_geometry()
    vis.poll_events()
    vis.update_renderer()
        # if save_image:
        #     vis.capture_screen_image("temp_%04d.jpg" % i)
    vis.destroy_window()
