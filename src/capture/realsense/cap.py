import cv2
import pyrealsense2 as rs2
import numpy as np

class Cap():
    def __init__(self):
        pass

    def get_angle(self, p1, p2):
        '''
        returns the angles between 2 points (angle between depth data)
        point format: (x,y,z)
        '''
        num = (p1[0]*p2[0] + p1[1]*p2[1] + p1[2] *p2[2])
        den = (np.sqrt( (p1[0]**2 + p1[1]**2 + p1[2]**2) * (p2[0]**2 + p2[1]**2 + p2[2]**2) ) )
        return np.arccos((num/den))

    def get_length(self, d1, d2, angle):
        # calculates distance of the unknown side of a triagle given
        # 2 sides and the angle between, the angle must be in radians
        return np.sqrt( d1**2 + d2**2 - (2 * d1 * d2) * np.cos(angle) )

    def euclid_dist(self, p1, p2):
        return np.sqrt((p1[0] - p2[0])**2 +
                (p1[1] - p2[0])**2 + 
                (p1[2] - p2[2])**2
                )

    def capture_data(self):
        """
        """
        pipeline = rs2.pipeline()

        # Start streaming
        pipeline.start(config)
        profile = pipeline.get_active_profile()

        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()

        depth_profile = rs2.video_stream_profile(profile.get_stream(rs2.stream.depth))
        depth_intrinsics = depth_profile.get_intrinsics()
        w, h = depth_intrinsics.width, depth_intrinsics.height

        # Processing blocks
        pc = rs2.pointcloud()
        decimate = rs2.decimation_filter()
        colorizer = rs2.colorizer()
        filters = [rs2.disparity_transform(),
                rs2.spatial_filter(),
                rs2.temporal_filter(),
                rs2.disparity_transform(False)]
        # Create a context object. This object owns the handles to all connected realsense devices
        success, frames = pipeline.try_wait_for_frames(timeout_ms=100)
        if not success:
            print("exiting")
            return
        depth_frame = frames.get_depth_frame()
        other_frame = frames.first(other_stream)

        depth_frame = decimate.process(depth_frame)

        # Grab new intrinsics (may be changed by decimation)
        depth_intrinsics = rs.video_stream_profile(
            depth_frame.profile).get_intrinsics()
        w, h = depth_intrinsics.width, depth_intrinsics.height

        depth_frame = decimate.process(depth_frame)

        for f in filters:
            depth_frame = f.process(depth_frame)

        # Create opencv window to render image in
        cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)

        # Streaming loop
        while True:
            # Get frameset of depth
            frames = pipeline.wait_for_frames()

            # Get depth frame
            depth_frame = frames.get_depth_frame()
            depth_data = frames.get_data()
            #distance in meters
            distance1 = depth_frame.get_distance(200,500)
            distance2 = depth_frame.get_distance(600,500)

            depth_intrinsics = rs2.video_stream_profile(
                depth_frame.profile).get_intrinsics()
            
            deproject1 = rs2.rs2_deproject_pixel_to_point(depth_intrinsics, [500, 500], distance1)
            deproject2 = rs2.rs2_deproject_pixel_to_point(depth_intrinsics, [600, 500], distance2)


            #print(deproject1)
            #print(deproject2)
            #depr = rs2.deproject_pixel_to_pointdeproject_pixel_to_point((500,500), distance)
            #5print(depr)
            #print(distance1)
            #print(distance2)

            dist = self.euclid_dist(deproject1, deproject2)
            print(dist)
            # Colorize depth frame to jet colormap
            depth_color_frame = rs2.colorizer().colorize(depth_frame)

            # Convert depth_frame to numpy array to render image in opencv
            depth_color_image = np.asanyarray(depth_color_frame.get_data())

            # Render image in opencv window
            cv2.imshow("Depth Stream", depth_color_image)
            key = cv2.waitKey(1)
            # if pressed escape exit program
            if key == 27:
                cv2.destroyAllWindows()
                break
        print("goodbye")
        
    def capture_colour(self):
        pipeline = rs2.pipeline()
        pipeline.start()
         # Streaming loop
        while True:
            # Get frameset of depth
            frames = pipeline.wait_for_frames()
            
            # Get depth frame
            frame = frames.get_depth_frame()
            # Colorize depth frame to jet colormap
            depth_color_frame = rs2.colorizer().colorize(depth_frame)

            # Convert depth_frame to numpy array to render image in opencv
            depth_color_image = np.asanyarray(depth_color_frame.get_data())

            # Render image in opencv window
            cv2.imshow("Video Stream", depth_color_image)
            key = cv2.waitKey(1)
            # if pressed escape exit program
            if key == 27:
                cv2.destroyAllWindows()
                break

        # Create opencv window to render image in
        cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)

    
    def depth2colour(self):
                
        # Create a pipeline
        pipeline = rs2.pipeline()

        #Create a config and configure the pipeline to stream
        #  different resolutions of color and depth streams
        config = rs2.config()
        config.enable_stream(rs2.stream.depth, 640, 360, rs2.format.z16, 30)
        config.enable_stream(rs2.stream.color, 640, 480, rs2.format.bgr8, 30)

        # Start streaming
        profile = pipeline.start(config)

        # Getting the depth sensor's depth scale (see rs2-align example for explanation)
        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        print("Depth Scale is: " , depth_scale)

        # We will be removing the background of objects more than
        #  clipping_distance_in_meters meters away
        clipping_distance_in_meters = 1 #1 meter
        clipping_distance = clipping_distance_in_meters / depth_scale

        # Create an align object
        # rs2.align allows us to perform alignment of depth frames to others frames
        # The "align_to" is the stream type to which we plan to align depth frames.
        align_to = rs2.stream.color
        align = rs2.align(align_to)

        # Streaming loop
        try:
            while True:
                # Get frameset of color and depth
                frames = pipeline.wait_for_frames()
                # frames.get_depth_frame() is a 640x360 depth image
                
                # Align the depth frame to color frame
                aligned_frames = align.process(frames)
                
                # Get aligned frames
                aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
                color_frame = aligned_frames.get_color_frame()
                
                # Validate that both frames are valid
                if not aligned_depth_frame or not color_frame:
                    continue
                
                depth_image = np.asanyarray(aligned_depth_frame.get_data())
                #color_image = np.asanyarray(color_frame.get_data())
                
                # Remove background - Set pixels further than clipping_distance to grey
                grey_color = 153
                depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
                bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)
                
                # Render images
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
                images = np.hstack((bg_removed, depth_colormap))
                cv2.namedWindow('Align Example', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('Align Example', images)
                key = cv2.waitKey(1)
                # Press esc or 'q' to close the image window
                if key & 0xFF == ord('q') or key == 27:
                    cv2.destroyAllWindows()
                    break
        finally:
            pipeline.stop()


if __name__ == "__main__":
    cap = Cap()
    cap.capture_data()