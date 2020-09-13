import pyrealsense2 as rs2
import open3d as o3d
import numpy as np
from load import get_file

def get_angle(p1, p2):
    '''
    Calculates the angles between 2 points in 3D space (angle between depth data)
    point format: (x,y,z)

    Formula(x1*x2 + y1*y2 + z1*z2)/sqrt( (x1^2 + y1^2 + z1^2) * (x2^2 +y2^2 + z2^2))
    '''
    num = (p1[0]*p2[0] + p1[1]*p2[1] + p1[2] *p2[2])
    den = (np.sqrt( (p1[0]**2 + p1[1]**2 + p1[2]**2) * (p2[0]**2 + p2[1]**2 + p2[2]**2) ) )
    return np.arccos((num/den))

def trangulate_dist(d1, d2, angle):
    ''' 
    Calculates the the unknown side of a triagle given 2 sides and the angle between. 
 
    Angle is in Radians

    Formula: sqrt(a^2 + c^2 - 2ac*cos(angle))
    '''
    return np.sqrt( d1**2 + d2**2 - (2 * d1 * d2) * np.cos(angle) )

def euclid_dist(p1, p2):
    '''
    Calculates euclidian distance between two points in 3D space.

    point format: tuple(x, y, z)

    Formula: sqrt((x1 - x2)^2 + (y1 -y2)^2 + (z1 - z2)^2)
    '''
    return np.sqrt((p1[0] - p2[0])**2 +
                (p1[1] - p2[0])**2 + 
                (p1[2] - p2[2])**2
                )

def get_length(intrinsics, pixel_1, pixel_2):
    '''
    intrinsics:
    depth_frame:
    pixel format: (x,y)

    NOTE: this function does not work. yet?
    '''

    #deproject from pixel to 3D point
    p1_deproject = rs2.rs2_deproject_pixel_to_point(intrinsics, pixel_1[:2], pixel_1[2])
    p2_deproject = rs2.rs2_deproject_pixel_to_point(intrinsics, pixel_2[:1], pixel_2[2])

    print(p1_deproject)
    print(p2_deproject)
    #calculate euclidian distance
    return euclid_dist(p1_deproject, p2_deproject)

def pick_points(pcd):
    print("")
    print(
        "1) Please pick at least two correspondences using [shift + left click]"
    )
    print("   Press [shift + right click] to undo point picking")
    print("2) Afther picking points, press q for close the window")

    print("Left click and drag to rotate around point.")
    print("Shift Left click and drag to rotate the screen left or right")
    print("Ctrl Left Click to pan")
    print()
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.run()  # user picks points
    vis.destroy_window()
    print("")
    #returns the inices of the users picked points
    return vis.get_picked_points()

def manual_measure(point_cloud):
    '''
    Creates an interface. Shift click the points you want to measure. Distance is calculated between each point selected. 
    
    Distance returned is in meters, though it prints out in both cm and m. 
    '''
    total_distance = 0
    distance_segments = []

    #picked points return the index of the points picked in the cloud
    picked_points = pick_points(point_cloud)
    print(picked_points)
    
    #convert pointcloud to array of points
    np_cloud = np.asarray(point_cloud.points)

    #for every pair of points, calculate the distance
    for point in range(len(picked_points)-1):

        p1 = np_cloud[picked_points[point]]
        p2 = np_cloud[picked_points[point+1]]
        
        #triangulate the distance between the two points
        angle = get_angle(p1,p2)
        distance = trangulate_dist(p1[2],p2[2],angle)
    
        print("Section " + str(point+1) + ": " + str(distance) + " meters")

        #distance = euclid_dist(p1, p2)
        distance_segments.append(distance)
        total_distance += distance

    print(str(total_distance * 100) + " centimeters")
    print(str(total_distance) + " meters")
    return total_distance, distance_segments, (p1,p2)

if __name__ == "__main__":
    import pandas

    calculated_distance = []#meters
    set_distance = [] #feet
    length = [] #cm
    body_part = []#string description
    file_name =[] #string name for capture number and camera
    note = []#notes about what the camera sees
    

    print("Starting...")

    # Grab new intrinsics (may be changed by decimation)
    #angle = get_angle((10,1,1), (1,1,0) )
    #length = get_length(3,2,angle)
    while True:
        cloud_path, cloud_format = get_file()
        cloud = o3d.io.read_point_cloud(cloud_path, format=cloud_format)
        #intrinsics = read_intrinsics((cloud_path[:-4] + "_intrinsics.txt"))
        length = manual_measure(cloud)
        print("Stopping...")