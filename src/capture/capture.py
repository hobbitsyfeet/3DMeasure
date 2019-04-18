import cv2
import pyrealsense2 as rs2
import numpy as np

class capture():
    def __init__(self):
        pass

    def capture_data(self):
        """
        """
        try:
            # Create a context object. This object owns the handles to all connected realsense devices
            pipeline = rs2.pipeline()
            pipeline.start()

            # Create opencv window to render image in
            cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)

            # Streaming loop
            while True:
                # Get frameset of depth
                frames = pipeline.wait_for_frames()

                # Get depth frame
                depth_frame = frames.get_depth_frame()

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
        finally:
            print("goodbye")
        
    

if __name__ == "__main__":
    cap = capture()