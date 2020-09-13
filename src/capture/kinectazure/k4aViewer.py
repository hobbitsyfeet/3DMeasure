import pyk4a
from pyk4a import Config, PyK4A, ColorResolution
from copy import deepcopy

import cv2
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
import matplotlib.pyplot as plt


def white_balance(img, avg_a=None, avg_b=None, setwb = False):
    result = img
    if setwb == True:
        result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        avg_a = np.average(result[:, :, 1])
        avg_b = np.average(result[:, :, 2])

        result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    elif avg_a != None and avg_b != None: 
        result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)

    return result, avg_a, avg_b

if __name__ == "__main__":
    
    wba = None
    wbb = None
    toggle_noise_redux = False


    k4a = PyK4A(Config(color_resolution=ColorResolution.RES_720P,
                    depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
                    synchronized_images_only=True, ))
    k4a.connect()


    # getters and setters directly get and set on device
    k4a.whitebalance = 4500
    assert k4a.whitebalance == 4500
    k4a.whitebalance = 4510
    assert k4a.whitebalance == 4510
    k4a.brightness = 126
    while 1:
        # img_color = k4a.get_capture(color_only=True)
        img_color, img_depth = k4a.get_capture()  # Would also fetch the depth image
        if np.any(img_color):
            #whitebalance

            key = cv2.waitKey(10)
            # if key != -1:
            #     cv2.destroyAllWindows()
            #     break
            if key == ord('w'):
                tmp = deepcopy(k4a.brightness)
                print(tmp)
                # k4a.brightness 
                img , wba, wbb = white_balance(img_color, setwb=True)
                print (tmp)
                k4a.brightness = tmp
                
            elif key == ord('c'):
                equ = cv2.equalizeHist(img_color)
                cv2.imshow(equ)
            elif key == ord('9'):
                print(k4a.brightness)
                k4a.brightness += 1
            
            elif key == ord('h'):
                img_color = cv2.resize(img_color, (50,50), interpolation = cv2.INTER_AREA) 
                print("creating image")
                img_color = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)
                b,g,r = cv2.split(img_color)
                print("creating plt")
                fig = plt.figure()
                axis = fig.add_subplot(1, 1, 1, projection="3d")
                pixel_colors = img_color.reshape((np.shape(img_color)[0]*np.shape(img_color)[1], 3))
                norm = colors.Normalize(vmin=-1.,vmax=1.)
                norm.autoscale(pixel_colors)
                pixel_colors = norm(pixel_colors).tolist()
                axis.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker=".")
                axis.set_xlabel("Red")
                axis.set_ylabel("Green")
                axis.set_zlabel("Blue")
                print("showing image")
                plt.show()

                hsv_img = cv2.cvtColor(img_color, cv2.COLOR_RGB2HSV)
                h, s, v = cv2.split(hsv_img)
                fig = plt.figure()
                axis = fig.add_subplot(1, 1, 1, projection="3d")
                axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
                axis.set_xlabel("Hue")
                axis.set_ylabel("Saturation")
                axis.set_zlabel("Value")
                plt.show()

                print(hsv_img)
            img_depth = ((img_depth - img_depth.min()) * (1/(img_depth.max() - img_depth.min()) * 255)).astype('uint8')

            img_color, avg_a, avg_b = white_balance(img_color, wba, wbb)

            
            cv2.imshow('k4a', img_color[:, :, :3])
            cv2.imshow('depth', img_depth)


            gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
            # Using the Canny filter to get contours
            edges = cv2.Canny(gray, 20, 30)
            # Using the Canny filter with different parameters
            edges_high_thresh = cv2.Canny(gray, 60, 120)
            # Stacking the images to print them together
            # For comparison
            # images = np.hstack((gray, edges, edges_high_thresh))

            # Display the resulting frame
            cv2.imshow('Frame', edges_high_thresh)


    k4a.disconnect()
