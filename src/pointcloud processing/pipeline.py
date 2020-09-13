import pcl
import open3d as o3d
import numpy as np
import load
import plane_segmentation
import eulcidian_cluster
import manual_registration
import filter_outliers
import measure_cloud
import global_registration
import reg_grow_segmentation
import convert
import resample
import voxel_grid
import time
import uuid
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from copy import deepcopy

if __name__ =="__main__":
    pre_clustered = False
    start_time = ""
    save_path = "F:/Data/Pipeline/" + start_time

    cloud_paths = load.get_files()

    registered_cloud = None
    
    manual_reg = False

    cloud_list = []


    #pre-load all files for processing
    for path in cloud_paths:
        #cloud_list.append(pcl.load(path,format="ply"))
        cloud_list.append(o3d.io.read_point_cloud(path))
        
    #target_cloud = pcl.load(cloud_paths[0],format="ply")
    target_cloud = o3d.io.read_point_cloud(path)
    
    #process each cloud
    counter = 0
    for point_cloud in cloud_list:
        print(point_cloud)

        #point_cloud = convert.pcl_to_o3d(point_cloud)

        if pre_clustered == False:
            eulcidian_cluster.cluster_and_select(point_cloud,point_cloud)
            #print("Eliminating horizontal planes...")
            #point_cloud = plane_segmentation.segment(point_cloud)
            
            #print("Clustering Clouds...")
            #point_cloud = eulcidian_cluster.cluster_and_select(point_cloud, point_cloud)

        # point_cloud = convert.pcl_to_o3d(point_cloud)

        
        # registered_cloud = manual_registration.register(cloud_cluster_1,cloud_cluster_2)
        if counter > 0:
            # NOTE automatic registration relies on downsizing for accurate results.
            print("Preparing clusters for registration")
            
            #point_cloud_current = convert.pcl_to_o3d(cloud_list[counter])
            #point_cloud_previous = convert.pcl_to_o3d(target_cloud)
            point_cloud_current = cloud_list[counter]
            point_cloud_previous = target_cloud

            # measure_cloud.manual_measure(point_cloud_current)
            # measure_cloud.manual_measure(point_cloud_previous)

            if manual_reg == False:

                voxel_size = 0.01 #5cm average
                
                source, target, source_down, target_down, source_fpfh, target_fpfh = \
                    global_registration.prepare_dataset(point_cloud_current, point_cloud_previous,voxel_size)

                print("Calculating Global Registration...")
                globally_registered_cloud = global_registration.execute_global_registration(source_down,target_down,
                                                                                            source_fpfh,target_fpfh,
                                                                                            voxel_size)
                print("Calculating ICP Registration...")
                result_icp = global_registration.refine_registration(source, target, 
                                                                    source_fpfh, target_fpfh,
                                                                    globally_registered_cloud.transformation,
                                                                    voxel_size)

                print("Transforming Source...")
                print(result_icp.transformation)
            else:
                result_icp = manual_registration.register(point_cloud_current,point_cloud_previous)

            point_cloud_current.transform(result_icp.transformation)
            registered_cloud = point_cloud_current + point_cloud_previous

            

            print(registered_cloud)
            print(point_cloud_current)
            print(point_cloud_previous)

        
            # o3d.io.write_point_cloud((save_path + "registered_cloud.ply"),registered_cloud, write_ascii=True, compressed=True)

            # if len(registered_cloud.points) > 100:
            o3d.io.write_point_cloud((save_path + "regeristered_prefilter_cloud.ply"),registered_cloud,write_ascii=True)
            target_cloud = o3d.io.read_point_cloud((save_path + "regeristered_prefilter_cloud.ply"),format="ply")
            
            registered_cloud = convert.o3d_to_pcl(registered_cloud)
            # registered_cloud = convert.o3d_to_pcl(registered_cloud)
            # pcl.save(registered_cloud,(save_path + "regeristered_prefilter_cloud.ply"), format="ply")
            # target_cloud = pcl.load(save_path + "regeristered_prefilter_cloud.ply")
            #remove outliers
            registered_cloud = filter_outliers.statistical_filter(registered_cloud)

            #smooth data
            registered_cloud = resample.smooth(registered_cloud,0.01)
        
            # average and reduce point size
            registered_cloud = voxel_grid.filter(registered_cloud,leaf_size=0.01) #0.1cm


            # target_cloud = deepcopy(point_cloud_current + point_cloud_previous)
            print("Saving...")
            pcl.save(registered_cloud,(save_path + "registered_cloud.ply"), format="ply")
            
            print("Measuring")
            measure_cloud.manual_measure(convert.pcl_to_o3d(registered_cloud))

            '''
            smoothness = ""

            PCA_results = []
            #Perform PCA on entire object
            df = pd.DataFrame(convert.pcl_to_numpy(registered_cloud))
            pca = PCA(n_components=3)
            pca.fit(df)
            # Store results of PCA in a data frame
            result = pd.DataFrame(pca.transform(df), columns=['PCA%i' % i for i in range(3)], index=df.index)
            print (result)
            PCA_results.append(deepcopy(result))
            #perform PCA on each cluster
            while(str(smoothness) is not ""):
                clusters = reg_grow_segmentation.segment(registered_cloud, float(smoothness),min_cluster=5, view=True)

                for cluster in clusters:
                    print("Starting Statistical Analysis...")
                    df = pd.DataFrame(convert.pcl_to_numpy(cluster))
                    pca = PCA(n_components=3)
                    pca.fit(df)
                    # Store results of PCA in a data frame
                    result = pd.DataFrame(pca.transform(df), columns=['PCA%i' % i for i in range(3)], index=df.index)
                    PCA_results.append(deepcopy(result))
                    print (result)
                
                smoothness = input()
            
            show_fig_flag = 0
            
            while show_fig_flag is not -1:
                # Plot initialisation
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.scatter(PCA_results[show_fig_flag]['PCA0'], PCA_results[show_fig_flag]['PCA1'], PCA_results[show_fig_flag]['PCA2'], cmap="Set2_r", s=60)
                
                # make simple, bare axis lines through space:
                xAxisLine = ((min(PCA_results[show_fig_flag]['PCA0']), max(PCA_results[show_fig_flag]['PCA0'])), (0, 0), (0,0))
                ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r')
                yAxisLine = ((0, 0), (min(PCA_results[show_fig_flag]['PCA1']), max(PCA_results[show_fig_flag]['PCA1'])), (0,0))
                ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r')
                zAxisLine = ((0, 0), (0,0), (min(PCA_results[show_fig_flag]['PCA2']), max(PCA_results[show_fig_flag]['PCA2'])))
                ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'r')
                
                # label the axes
                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.set_zlabel("Z")
                ax.set_title("")
                
                plt.show(block=False)
                
                print("Which cluster would you like to see? Enter -1 to continue")
                show_fig_flag = int(input())


            #convert to o3d to measure
            # registered_cloud = convert.pcl_to_o3d(registered_cloud)

            print("Starting Statistical Analysis...")
            df = pd.DataFrame(convert.pcl_to_numpy(registered_cloud))
            pca = PCA(n_components=3)
            pca.fit(df)
            # Store results of PCA in a data frame
            result = pd.DataFrame(pca.transform(df), columns=['PCA%i' % i for i in range(3)], index=df.index)
            print (result)

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
            ax.set_xlabel("Width")
            ax.set_ylabel("Height")
            ax.set_zlabel("Depth")
            ax.set_title("")
            plt.show(block=False)
            '''

           
            

        counter += 1


    








    


