from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture


import cv2
import pyrealsense2 as rs2
import numpy as np
class CamApp(App):

    def build(self):
        self.img1=Image()
        layout = BoxLayout()
        layout.add_widget(self.img1)

        self.pipeline = rs2.pipeline()
        self.pipeline.start()
        self.img2=Image()
        layout.add_widget(self.img2)

        #CV2
        self.capture = cv2.VideoCapture(1)
        Clock.schedule_interval(self.update, 1.0/33.0)

        return layout

    def update(self, dt):
        #capture the frames needed for 
        frames = self.pipeline.wait_for_frames()
        # Get depth frame
        depth_frame = frames.get_depth_frame()
        # Colorize depth frame to jet colormap
        depth_color_frame = rs2.colorizer().colorize(depth_frame)
        # Convert depth_frame to numpy array to render image in opencv
        depth_color_image = np.asanyarray(depth_color_frame.get_data())
        # Render image in opencv window
        # cv2.imshow("Depth Stream", depth_color_image)
        buf2 = cv2.flip(depth_color_image, 0)
        buf = buf2.tostring()
        texture2 = Texture.create(size=(depth_color_image.shape[1], depth_color_image.shape[0]), colorfmt='bgr')
        texture2.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        # display image from cam in opencv window
        ret, frame = self.capture.read()
        # cv2.imshow("CV2 Image", frame)
        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        # display image from the texture
        self.img1.texture = texture1
        # display image from the texture
        self.img2.texture = texture2

if __name__ == '__main__':
    CamApp().run()