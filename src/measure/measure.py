import pyrealsense2 as rs2
import numpy as np

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
    Calculates the the unknown side of a triagle given
    2 sides and the angle between, 
    
    Angle is in Radians

    Formula: sqrt(a^2 + c^2 - 2ac*cos(angle))
    '''
    return np.sqrt( d1**2 + d2**2 - (2 * d1 * d2) * np.cos(angle) )

def euclid_dist(p1, p2):
    '''
    Calculates euclidian distance between two points in 3D space
    point format: (x,y,z)

    Formula: sqrt((x1 - x2)^2 + (y1 -y2)^2 + (z1 - z2)^2)
    '''
    return np.sqrt((p1[0] - p2[0])**2 +
                (p1[1] - p2[0])**2 + 
                (p1[2] - p2[2])**2
                )

def get_length(intrinsics, depth_frame, pixel_1, pixel_2):
    '''
    intrinsics:
    depth_frame:
    pixel format: (x,y)
    '''
    #get distances of specified pixels
    p1_dist = depth_frame.get_distance(pixel_1)
    p2_dist = depth_frame.get_distance(pixel_2)

    #deproject from pixel to 3D point
    p1_deproject = rs2.rs2_deproject_pixel_to_point(intrinsics, pixel_1, p1_dist)
    p2_deproject = rs2.rs2_deproject_pixel_to_point(intrinsics, pixel_2, p2_dist)

    #calculate euclidian distance
    euclid_dist()
    
if __name__ == "__main__":
    print("Starting...")
    
    # Grab new intrinsics (may be changed by decimation)
    angle = get_angle((10,1,1), (1,1,0) )
    length = get_length(3,2,angle)

    print(length)
    print(angle)
    print("Stopping...")