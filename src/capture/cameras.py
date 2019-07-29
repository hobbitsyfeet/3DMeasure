import pyrealsense2 as rs
import numpy as np
import cv2
# import open3d as o3d
import pcl
from pcl import pcl_visualization


# Configure depth and color streams...
# ...from Camera 1
pipeline_1 = rs.pipeline()
config_1 = rs.config()
config_1.enable_device('816612061111')
config_1.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config_1.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
# ...from Camera 2
pipeline_2 = rs.pipeline()
config_2 = rs.config()
config_2.enable_device('816612061344')
config_2.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config_2.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)


# Start streaming from both cameras
pipeline_1.start(config_1)
pipeline_2.start(config_2)

profile_1 = pipeline_1.get_active_profile()
profile_2 = pipeline_2.get_active_profile()

# depth_sensor_1 = profile_1.get_device().first_depth_sensor()
# depth_sensor_2 = profile_2.get_device().first_depth_sensor()
# depth_scale_1 = depth_sensor_1.get_depth_scale()
# depth_scale_2 = depth_sensor_2.get_depth_scale()

depth_profile_1 = rs.video_stream_profile(profile_1.get_stream(rs.stream.depth))
depth_profile_2 = rs.video_stream_profile(profile_2.get_stream(rs.stream.depth))

depth_intrinsics_1 = depth_profile_1.get_intrinsics()
depth_intrinsics_2 = depth_profile_2.get_intrinsics()

w1, h1 = depth_intrinsics_1.width, depth_intrinsics_1.height
w2, h2 = depth_intrinsics_2.width, depth_intrinsics_2.height

pc_1 = rs.pointcloud()
pc_2 = rs.pointcloud()
decimate = rs.decimation_filter()
decimate.set_option(rs.option.filter_magnitude, 2)
global save_index
save_index = 0
save_path = "./data/"
colorizer_1 = rs.colorizer()
colorizer_2 = rs.colorizer()

# filters = [rs.disparity_transform(),
#                 rs.spatial_filter(),
#                 rs.temporal_filter(),
#                 rs.disparity_transform(False)]

def nothing(x):
    pass
# def o3d_view_pointcloud(path_1, path_2):
#     o3d_cloud1 = o3d.io.read_point_cloud(path_1, format="ply")
#     o3d_cloud2 = o3d.io.read_point_cloud(path_2, format="ply")
#     o3d.visualization.draw_geometries([o3d_cloud1, o3d_cloud2])

def view_pointcloud(path_1, path_2):
    pcl_cloud1 = pcl.load_XYZRGB(path_1, format="ply")
    pcl_cloud2 = pcl.load_XYZRGB(path_2, format="ply")
    viewer = pcl_visualization.CloudViewing()
    viewer.ShowColorCloud(pcl_cloud1)
    # viewer.ShowColorCloud(pcl_cloud2)
    v = True
    while v:
        v = not(viewer.WasStopped())
    # pcl.save(cloud,"./data/Best2_Scaled_Monkey.ply",format="ply",binary=False)
def get_depth_data(frame_1, frame_2):
        # frames_1 = pipeline_1.wait_for_frames()
        depth_frame_1 = frame_1.get_depth_frame()
        color_frame_1 = frame_1.get_color_frame()

        depth_frame_1 = decimate.process(depth_frame_1)

        # Convert images to numpy arrays
        depth_image_1 = np.asanyarray(depth_frame_1.get_data())
        color_image_1 = np.asanyarray(color_frame_1.get_data())
        colorized_depth_1 = colorizer_1.colorize(depth_frame_1)
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap_1 = np.asanyarray(colorized_depth_1.get_data())
        # depth_colormap_1 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image_1, alpha=0.5), cv2.COLORMAP_JET)

        # Camera 2
        # Wait for a coherent pair of frames: depth and color
        frames_2 = pipeline_2.wait_for_frames()
        depth_frame_2 = frames_2.get_depth_frame()
        color_frame_2 = frames_2.get_color_frame()


        depth_frame_1 = decimate.process(depth_frame_1)
        depth_frame_2 = decimate.process(depth_frame_2)

        # for f in filters:
        #         depth_frame_1 = f.process(depth_frame_1)
        #         depth_frame_2 = f.process(depth_frame_2)

        # Convert images to numpy arrays
        depth_image_2 = np.asanyarray(depth_frame_2.get_data())
        color_image_2 = np.asanyarray(color_frame_2.get_data())
        colorized_depth_2 = colorizer_2.colorize(depth_frame_2)
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap_2 = np.asanyarray(colorized_depth_2.get_data())
        depth_colormap_2 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image_2, alpha=0.5), cv2.COLORMAP_JET)
        # Stack all images horizontally
        mapped_frame_1, color_source_1 = color_frame_1, color_image_1
        mapped_frame_2, color_source_2 = color_frame_2, color_image_2

        points_1 = pc_1.calculate(depth_frame_1)
        points_2 = pc_2.calculate(depth_frame_2)

        pc_1.map_to(mapped_frame_1)
        pc_2.map_to(mapped_frame_2)

        return points_1, points_2, mapped_frame_1, mapped_frame_2


def save(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global save_index
        save_index+=1
        points_1, points_2, mapped_frame_1, mapped_frame_2 = get_depth_data(param[0],param[1])
        # points_2, mapped_frame_2 = get_depth_data(param[1])
        print((save_path + "816612061111_no"+str(save_index)+ ".ply"))
        print((save_path + "816612061344_no"+str(save_index)+ ".ply"))
        points_1.export_to_ply((save_path + "816612061111_no"+str(save_index)+".ply"),mapped_frame_1)
        points_2.export_to_ply((save_path + "816612061344_no"+str(save_index)+".ply"),mapped_frame_2)

        # o3d_view_pointcloud((save_path + "816612061111_no"+str(save_index)+".ply"),
        #                     (save_path + "816612061344_no"+str(save_index)+".ply"))


        view_pointcloud((save_path + "816612061111_no"+str(save_index)+".ply"),
                        (save_path + "816612061344_no"+str(save_index)+".ply"))

       
        print("Saved")

switch = '0 : OFF \n1 : ON'



cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)
cv2.resizeWindow('RealSense', 1000,480)

cv2.createTrackbar(switch, 'RealSense',0,1, nothing)

try:
    #This initialization loads up the first frame to all the global values.
    #This is done because the first process does not load the colour data over the point data.
    #I dont know why.
    print("Preforming initial Check...")
    frames_1 = pipeline_1.wait_for_frames()
    frames_2 = pipeline_2.wait_for_frames()
    get_depth_data(frames_1, frames_2)
    print("Initial test complete...")

    while cv2.getWindowProperty('RealSense', 1) >=0 :

        #collect and process only the colour frames for viewing
        frames_1 = pipeline_1.wait_for_frames()

        color_frame_1 = frames_1.get_color_frame()

        color_image_1 = np.asanyarray(color_frame_1.get_data())
   
        frames_2 = pipeline_2.wait_for_frames()

        color_frame_2 = frames_2.get_color_frame()

        color_image_2 = np.asanyarray(color_frame_2.get_data())

        cv2.waitKey(1)

        color_image_1 = cv2.cvtColor(color_image_1, cv2.COLOR_BGR2RGB)
        color_image_2 = cv2.cvtColor(color_image_2, cv2.COLOR_BGR2RGB)
        images = np.hstack((color_image_1,color_image_2))

        # Show images from both cameras
        if(cv2.getTrackbarPos(switch,'RealSense')) == -1:
            break
        
        cv2.imshow('RealSense', images)
        
        cv2.setMouseCallback('RealSense', save, [frames_1, frames_2])
       
        s = cv2.getTrackbarPos(switch,'RealSense')

        # Save images and depth maps from both cameras by turning on the switch
        if s==1:
            save_index += 1
            print((save_path + "816612061111_no"+str(save_index)+ ".ply"))
            print((save_path + "816612061344_no"+str(save_index)+ ".ply"))
            points_1, points_2, mapped_frame_1, mapped_frame_2 = get_depth_data(frames_1, frames_2)

            points_1.export_to_ply((save_path + "816612061111_no"+str(save_index)+ ".ply"), mapped_frame_1)
            points_2.export_to_ply((save_path + "816612061344_no"+str(save_index)+ ".ply"), mapped_frame_2)
            # view_pointcloud((save_path + "816612061344_no"+str(save_index)+ ".ply"),(save_path + "816612061344_no"+str(save_index)+ ".ply"))
            print ("Save")


            

finally:

    # Stop streaming
    pipeline_1.stop()
    pipeline_2.stop()

