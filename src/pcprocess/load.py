
import numpy as np
from tkinter import filedialog
from tkinter import Tk
import glob
import ntpath
import open3d as o3d

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def get_files_from_folder(folder_path = None, extension="ply"):
    """
    Gets all of the the specified type within the immediate folder (no deeper)
    """
    if folder_path is None:
        #close the tkinter window that pops up
        root = Tk()
        root.withdraw()
        print("loading file")

        folder_path = filedialog.askdirectory()
        print(folder_path)

    #get all files with extension in file_path
    file_list = [f for f in glob.glob( folder_path+"/" + "*." + extension)]

    return file_list


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

def get_files(file_path = None):
    """
    This function opens a file selection, and loads up the video selected.
    """
    if file_path is None:
        #close the tkinter window that pops up
        root = Tk()
        root.withdraw()
        print("loading file")

        dlg = filedialog.askopenfilenames()

    return list(root.tk.splitlist(dlg))


if __name__ == "__main__":

    while True:
        pc_type = None
        try:
            file_path, file_format = get_file()
        except:
            break
        
        pcd = o3d.io.read_point_cloud(file_path, format=file_format)

        o3d.draw_geometries([pcd])