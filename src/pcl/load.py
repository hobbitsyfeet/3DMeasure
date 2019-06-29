import pcl
from pcl import pcl_visualization
import numpy as np
import open3d
from tkinter import filedialog
from tkinter import Tk

def get_file(file_path = None):
    """
    This function opens a file selection, and loads up the video selected.
    """
    if file_path is None:
        #close the tkinter window that pops up
        root = Tk()
        root.withdraw()
        print("loading file")

        dlg = filedialog.Open()
        file_path = dlg.show()

    #extract the file format from extentsion
    file_format = file_path[file_path.find(".")+1:]

    print(file_path)
    if file_path != '':
        return file_path, file_format

if __name__ == "__main__":
    file_path, file_format = get_file()
    print("hecc")

    cloud = pcl.load(file_path, format=file_format)
    # centred = cloud - np.mean(cloud, 0)
    # # print(centred)
    # ptcloud_centred = pcl.PointCloud()
    # ptcloud_centred.from_array(centred)
    print(cloud)

    visual = pcl.pcl_visualization.CloudViewing()
    
    # PointXYZ
    visual.ShowMonochromeCloud(cloud, b'cloud')
    # visual.ShowGrayCloud(ptcloud_centred, b'cloud')
    # visual.ShowColorCloud(ptcloud_centred, b'cloud')
    # visual.ShowColorACloud(ptcloud_centred, b'cloud')

    v = True
    while v:
        v = not(visual.WasStopped())