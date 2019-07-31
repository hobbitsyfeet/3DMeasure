import pcl
import numpy as np
from pcl import pcl_visualization
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

def get_pcl_from_numpy(file_path):
    np_cloud = np.load(file_path)
    print("Scaling point distance down...")
    print(np_cloud[0])
    temp_cloud = np_cloud

    #Calculated measurments to match scale of the thickness and .
    for point in range(len(np_cloud)):
        temp_cloud[point] = np_cloud[point] * np.asarray([0.0011,0.0011,0.0011])
 
    print(temp_cloud[0])
    print("Done Scaling")
    #the most important step, converting double to float. PCL does not support double
    new_np_cloud = temp_cloud.astype('float32')
    
    pcl_cloud = pcl.PointCloud()
    pcl_cloud.from_array(new_np_cloud)
    return pcl_cloud
    

if __name__ == "__main__":
    
    while True:
        pc_type = None
        try:
            file_path, file_format = get_file()
        except:
            break
        try:
            cloud = pcl.load_XYZRGB(file_path, format=file_format)
            pc_type = "colour"
        except:
            print("Could not load Colour Pointcloud, trying monochrome.")
            try:
                cloud = pcl.load(file_path, format=file_format)
                pc_type = "monochrome"
            except:
                print("Could not load monochrome Pointcloud into pcl_cloud, trying numpy")
                cloud = get_pcl_from_numpy(file_path)
                pc_type = "numpy"

        
        visual = pcl.pcl_visualization.CloudViewing()
        
        # # PointXYZ
        if pc_type == "colour":
            visual.ShowColorCloud(cloud, b'cloud')
        else:
            visual.ShowMonochromeCloud(cloud, b'cloud')
        # # visual.ShowGrayCloud(ptcloud_centred, b'cloud')
        
        # # visual.ShowColorACloud(cloud, b'cloud')
        # # cloud.make_NormalEstimation()
        v = True
        while v:
            v = not(visual.WasStopped())
        # pcl.save(cloud,"./data/Best2_Scaled_Monkey.ply",format="ply",binary=False)