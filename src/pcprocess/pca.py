    
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from copy import deepcopy
import load
import numpy as np
import convert
import pcl
import open3d as o3d

def get_centroid(cloud):
    """
    Calculates the average value for each dimension in 3D space.
    """
    try: 
        np_cloud = convert.pcl_to_numpy(cloud)
    except:
        np_cloud = convert.o3d_to_numpy(cloud)
    
    avg_x = 0
    avg_y = 0
    avg_z = 0

    print(np_cloud.shape)
    for point in np_cloud:
        # print(point)
        avg_x += point[0]
        avg_y += point[1]
        avg_z += point[2]

    avg_x = avg_x / np_cloud.shape[0]
    avg_y = avg_y / np_cloud.shape[0]
    avg_z = avg_z / np_cloud.shape[0]

    return (avg_x, avg_y, avg_z)

def get_pca(cloud):
    """
    Calculates the Principal components for 3 dimensions and returns the vectors, centroid and pca trandform result.
    """
    df = None

    #Convert clouds to numpy format
    try: 
        df = pd.DataFrame(convert.pcl_to_numpy(cloud))
    except:
        df = pd.DataFrame(convert.o3d_to_numpy(cloud))

    # get cloud centre
    centroid = get_centroid(cloud)

    # calculate PCA for each dimension
    pca = PCA(n_components=3)
    pca.fit(df)

    # get PCA results
    result = pd.DataFrame(pca.transform(df), columns=['PCA%i' % i for i in range(3)], index=df.index)

    vx = (min(result['PCA0']), max(result['PCA0']))
    vy = (min(result['PCA1']), max(result['PCA1']))
    vz = (min(result['PCA0']), max(result['PCA2']))

    # calculate lenths of each pca
    lengths = (abs(vx[1] - vx[0]), abs(vy[1] - vy[0]), abs(vz[1] - vz[0]) )

    # generate vector objects which represent the object
    vectors = []
    i = 0
    for length, vector in zip(pca.explained_variance_, pca.components_):

        # no clue why this works.... but + centroid translates each dimension to center of object rather than origin (0,0,0)
        v = vector * 2 * np.sqrt(length) + centroid
        vectors.append(v)
        i += 1

    return vectors, centroid, result

def o3d_pca_geometry(vectors, center):
    """
    Generates open3d lineset objects for the pca vectors created around the center of the 3D pointcloud.
    """
    # separate each vector
    vx = vectors[0]
    vy = vectors[1]
    vz = vectors[2]

    # set 4 points, the end points of each vector and the centroid
    points = [
                center, vx, vy, vz
            ]
    # set the lines to go from center to each point
    lines = [
        [0,1],
        [0,2],
        [0,3],
    ]
    #each vector is red, green blue are PCA1, PCA2 and PCA3 respectivley.
    colors = [ [1,0,0], [0,1,0], [0,0,1]]

    #create open3d linesets.
    line_set = o3d.LineSet()
    line_set.points = o3d.Vector3dVector(points)
    line_set.lines = o3d.Vector2iVector(lines)
    line_set.colors = o3d.Vector3dVector(colors)

    return line_set


if __name__ == "__main__":


    cloud_path, cloud_format = load.get_file()
    # cloud = pcl.load(cloud_path,cloud_format)
    cloud = o3d.io.read_point_cloud(cloud_path, format="ply")

    #Perform PCA on entire object
    vectors, center, result = get_pca(cloud)

    #create vectors in o3d linesets
    line_set = o3d_pca_geometry(vectors, center)

    #display in o3d
    o3d.draw_geometries([cloud, line_set])
