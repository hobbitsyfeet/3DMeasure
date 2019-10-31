import pyrealsense2 as rs
import numpy as np
import cv2
import open3d as o3d
import argparse
import os
from time import strftime
#from cv_track import track
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--all_filters', type=bool, default=False, help='Enables all post-processing filters to enhace quality and reduce noise. Spatial, Temporal and Disparity Transform')
parser.add_argument('--spatial', '-s', type=bool, default=True, help='Enables smoothing that preserves edges.')
parser.add_argument('--temporal', '-t', type=bool, default=True, help='Smooths/improves depth data by sampling previous frames. Best used with static scene due to blurriung')
parser.add_argument('--disparity', type=bool, default=False, help="Only if you're dispair_ate.")
parser.add_argument('--decimation' , '-d', type=int, default=2, help="Reduces resolution, and averages out depth of downsampled data.")
parser.add_argument('--output', '-o', type=str, default='C:/Users/Justin/Documents/Github/3DMeasure/', help="Where to write the data")
parser.add_argument('--config', type=str, default='')
FLAGS = parser.parse_args()
ALL_FILTERS = FLAGS.all_filters
SPATIAL = FLAGS.spatial
TEMPORAL = FLAGS.temporal
DISPARITY = FLAGS.disparity
DECIMATION = FLAGS.decimation



jsonObj = json.load(open(self.jsonFile))
self.json_string = str(jsonObj).replace("'", '\"')
def loadConfiguration(self):
	self.dev = self.cfg.get_device()
	self.advnc_mode = rs.rs400_advanced_mode(self.dev)

	print("Advanced mode is", "enabled" if self.advnc_mode.is_enabled() else "disabled")
	self.advnc_mode.load_json(self.json_string)

#tracker = track()
save_path = "./data/"
#zipfile name is the Year/Month/Day-Hour/Minute started.
zip_dir_name = save_path + strftime("%Y-%m-%d_%H-%M-%S")

#code to zip files
# Declare the function to return all file paths of the particular directory
def retrieve_file_paths(dirName):
 
    # setup file paths variable
    file_paths = []

    # Read all directory, subdirectories and file lists
    for file in os.listdir(save_path):
        if file.endswith(".ply"):
            # # Create the full filepath by using os module.
            file_path = os.path.join(save_path, file)
            if file_path[file_path.find("."):] != ".zip":

                file_paths.append(file_path)
                
    # return all paths
    return file_paths
 
# import pcl
# from pcl import pcl_visualization

CV2_LBUTTON_FLAG = False

# Configure depth and color streams...
# ...from Camera 1
pipelines = []
configs = []
profiles = []


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
decimate1 = rs.decimation_filter()
decimate2 = rs.decimation_filter()
decimate1.set_option(rs.option.filter_magnitude, DECIMATION)
decimate2.set_option(rs.option.filter_magnitude, DECIMATION)
global save_index
save_index = 0


colorizer_1 = rs.colorizer()
colorizer_2 = rs.colorizer()

filters = [
                #rs.disparity_transform(),
                rs.spatial_filter(),
                #rs.temporal_filter(),
                #rs.disparity_transform(False)
                ]
# if DISPARITY:
#     filters.append(rs.disparity_transform())
# if SPATIAL:
#     rs.spatial_filter()
def nothing(x):
    pass

def set_CVLBUTTON_FLAG(event):
    global CV2_LBUTTON_FLAG
    if event != 0  and event != cv2.EVENT_LBUTTONDBLCLK:
        if event == cv2.EVENT_LBUTTONDOWN:
            print("SETTING CV_LBUTTON_FLAG TRUE")
            CV2_LBUTTON_FLAG = True

        if event == cv2.EVENT_LBUTTONUP:
            print("SETTING CV_LBUTTON_FLAG FALSE")
            CV2_LBUTTON_FLAG = False



def o3d_view_pointcloud(path_1, path_2):
    """
    View two pointlcouds from a their paths in one Open3D visualization.
    """
    o3d_cloud1 = o3d.io.read_point_cloud(path_1, format="ply")
    o3d_cloud2 = o3d.io.read_point_cloud(path_2, format="ply")
    o3d.visualization.draw_geometries([o3d_cloud1, o3d_cloud2])

# def view_pointcloud(path_1, path_2):
#     pcl_cloud1 = pcl.load_XYZRGB(path_1, format="ply")
#     pcl_cloud2 = pcl.load_XYZRGB(path_2, format="ply")
#     viewer = pcl_visualization.CloudViewing()
#     viewer.ShowColorCloud(pcl_cloud1)
#     viewer.ShowColorCloud(pcl_cloud2)
#     v = True
#     while v:
#         v = not(viewer.WasStopped())


def get_depth_data(frame_1, frame_2, color_frame_1, color_frame_2):
    """
    Returns depth data ready to export. 
    This depth data is processed and has the respective colour images mapped onto them.
    """
    # frames_1 = pipeline_1.wait_for_frames()
    depth_frame_1 = frame_1.get_depth_frame()
    depth_frame_2 = frame_2.get_depth_frame()
    
    # depth_image_1 = np.asanyarray(depth_frame_1.get_data())
    # depth_image_2 = np.asanyarray(depth_frame_2.get_data())

    color_image_1 = np.asanyarray(color_frame_1.get_data())
    color_image_2 = np.asanyarray(color_frame_2.get_data())
    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)

    #NOTE This is what reduces the pointcloud density.
    depth_frame_1 = decimate1.process(depth_frame_1)
    depth_frame_2 = decimate2.process(depth_frame_2)

    for f in filters:
         depth_frame_1 = f.process(depth_frame_1)
         depth_frame_2 = f.process(depth_frame_2)

    # Convert images to numpy arrays

    colorized_depth_1 = colorizer_1.colorize(depth_frame_1)
    colorized_depth_2 = colorizer_2.colorize(depth_frame_2)
    
    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap_1 = np.asanyarray(colorized_depth_1.get_data())
    depth_colormap_2 = np.asanyarray(colorized_depth_2.get_data())
    
    # Stack all images horizontally
    mapped_frame_1, color_source_1 = color_frame_1, color_image_1
    mapped_frame_2, color_source_2 = color_frame_2, color_image_2

    points_1 = pc_1.calculate(depth_frame_1)
    points_2 = pc_2.calculate(depth_frame_2)

    pc_1.map_to(mapped_frame_1)
    pc_2.map_to(mapped_frame_2)

    return points_1, points_2, mapped_frame_1, mapped_frame_2


def save(event,x,y,flags,param):
    """
    This function is designed to work with CV2 callback. 

    Double left click saves and displays the pointcloud.

    Left click only saves. If held, it shoud continuously save data.
    """
    set_CVLBUTTON_FLAG(event)
    global save_index
    # check if it was double click first, if so, save and display.
    if event == cv2.EVENT_LBUTTONDBLCLK:
        save_index+=1
        points_1, points_2, mapped_frame_1, mapped_frame_2 = get_depth_data(param[0],param[1], param[2], param[3])
        print((save_path + "816612061111_no"+str(save_index)+ ".ply"))
        print((save_path + "816612061344_no"+str(save_index)+ ".ply"))
        points_1.export_to_ply((save_path + "816612061111_no"+str(save_index)+".ply"),mapped_frame_1)
        points_2.export_to_ply((save_path + "816612061344_no"+str(save_index)+".ply"),mapped_frame_2)

        o3d_view_pointcloud((save_path + "816612061111_no"+str(save_index)+".ply"),
                            (save_path + "816612061344_no"+str(save_index)+".ply"))
        print("Saved")
        # view_pointcloud((save_path + "816612061111_no"+str(save_index)+".ply"),
        #                 (save_path + "816612061344_no"+str(save_index)+".ply"))

    # # Otherwise check and see if left button is down (no double click) and simply save.
    # # If left click is held down, it shoud record continuously
    # elif CV2_LBUTTON_FLAG:
    #     save_index+=1
    #     points_1, points_2, mapped_frame_1, mapped_frame_2 = get_depth_data(param[0],param[1], param[2], param[3])
    #     print((save_path + "816612061111_no"+str(save_index)+ ".ply"))
    #     print((save_path + "816612061344_no"+str(save_index)+ ".ply"))
    #     points_1.export_to_ply((save_path + "816612061111_no"+str(save_index)+".ply"),mapped_frame_1)
    #     points_2.export_to_ply((save_path + "816612061344_no"+str(save_index)+".ply"),mapped_frame_2)
    #     print("Saved")
    

# name for the trackbar. This also acts as the toggle variable.
switch = '0 : OFF \n1 : ON'


#create the cv2 window for display then make it fullscreen
cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)
# cv2.setWindowProperty('Realsense', cv2.WINDOW_NORMAL, cv2.WINDOW_FULLSCREEN)
cv2.resizeWindow('RealSense',  2560 , 1440)

cv2.createTrackbar(switch, 'RealSense',0,1, nothing)

try:
    #This initialization loads up the first frame to all the global values.
    #This is done because the first process does not load the colour data over the point data.
    #I dont know why.
    print("Preforming initial Check...")
    frames_1 = pipeline_1.wait_for_frames()
    frames_2 = pipeline_2.wait_for_frames()
    color_frame_1 = frames_1.get_color_frame()
    color_frame_2 = frames_2.get_color_frame()
    get_depth_data(frames_1, frames_2, color_frame_1, color_frame_2)
    print("Initial test complete...")

    # Continuously display the colour frames from the RGB camera on the D415 cameras.
    while cv2.getWindowProperty('RealSense', 1) >= 0 :

        #collect and process only the colour frames for viewing
        frames_1 = pipeline_1.wait_for_frames()
        color_frame_1 = frames_1.get_color_frame()
        color_image_1 = np.asanyarray(color_frame_1.get_data())
   
        frames_2 = pipeline_2.wait_for_frames()
        color_frame_2 = frames_2.get_color_frame()
        color_image_2 = np.asanyarray(color_frame_2.get_data())

        #needed for a break for viewing
        cv2.waitKey(1)
        # try:
        # color_image_1 = tracker.detect_model(color_image_1)
        # color_image_2 = tracker.detect_model(color_image_2)
        # except:
        #     print("could not detect on image 1")
        # try:
            # output = tracker.detect_model(color_image_2)
            # color_image_1, tracker_dimentions = tracker.show_detection(output, color_image_2)
            # print(color_image_1)
        # except:
            # print("could not detect on image 2")

        #colour images prepped to display throu CV2
        color_image_1 = cv2.cvtColor(color_image_1, cv2.COLOR_BGR2RGB)
        color_image_2 = cv2.cvtColor(color_image_2, cv2.COLOR_BGR2RGB)



        images = np.hstack((color_image_1,color_image_2))

        #Use the trackbar existance to check if the X has been selected. Quits the program.
        if(cv2.getTrackbarPos(switch,'RealSense')) == -1:
            break
        
        #display the images
        

        cv2.imshow('RealSense', images)
        
        #using CV2 callback, save the images
        
        cv2.setMouseCallback('RealSense', save, [frames_1, frames_2, color_frame_1, color_frame_2])
       
        s = cv2.getTrackbarPos(switch,'RealSense')

        # Save images and depth maps from both cameras by turning on the switch

        if s==1 or CV2_LBUTTON_FLAG:
            save_index += 1
            print((save_path + "816612061111_no"+str(save_index)+ ".ply"))
            print((save_path + "816612061344_no"+str(save_index)+ ".ply"))
            points_1, points_2, mapped_frame_1, mapped_frame_2 = get_depth_data(frames_1, frames_2, color_frame_1, color_frame_2)

            points_1.export_to_ply((save_path + "816612061111_no"+str(save_index)+ ".ply"), mapped_frame_1)
            points_2.export_to_ply((save_path + "816612061344_no"+str(save_index)+ ".ply"), mapped_frame_2)
            print ("Save")


            

finally:

    # Stop streaming
    pipeline_1.stop()
    pipeline_2.stop()

    print("Exporting into Zip")
    filePaths = retrieve_file_paths(save_path)
    # writing files to a zipfile
    zip_file = zipfile.ZipFile(zip_dir_name +'.zip', 'w', zipfile.ZIP_DEFLATED)
    with zip_file:
        # writing each file one by one
        for file in filePaths:
            arcname = file[file.rfind('/')+1:]
            print("Writing " + file ,end="...")
            zip_file.write(file,arcname=arcname)
            os.remove(file)
            print("Removed from dir.")
        print(zip_dir_name+'.zip file is created successfully!')