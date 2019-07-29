# %reload_ext signature
# %matplotlib inline

import numpy as np
import pydicom
from pydicom.dicomio import dcmread
import pydicom.uid
import os
import matplotlib.pyplot as plt
from glob import glob
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import scipy.ndimage
from skimage import morphology
from skimage import measure
from skimage.transform import resize
from sklearn.cluster import KMeans
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.tools import FigureFactory as FF
from plotly.graph_objs import *
init_notebook_mode(connected=True) 

data_path = "C:/Users/legom/Documents/GitHub/3DMeasure/data/PRICT-28/series_7/"
output_path = working_path = "C:/Users/legom/Documents/GitHub/3DMeasure/data/PRICT-28/Preprocess"
g = glob(data_path + '/*.dcm')

# Print out the first 5 file names to verify we're in the right folder.
print ("Total of %d DICOM images.\nFirst 5 filenames:" % len(g))
print ('\n'.join(g[:5]))

    #      
# Loop over the image files and store everything into a list.
# 

def load_scan(path):
    dirname = path
    files = os.listdir(dirname)
    # print(files)
    slices = []
    for file in files:
        try:
            dicom_file = pydicom.dcmread(fp=(path + file), force=True)
            dicom_file.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
            dicom_file.pixel_array
            slices.append(dicom_file)
            
            
        except:
            "Cannot Load Slice... Skipping"
            continue

    # print(slices)
    # slices = [pydicom.dcmread(data_path)(path + '/' + s) for s in os.listdir(path)]
    # print (slices)
    slices.sort(key = lambda x: int(x.InstanceNumber))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
        
    for s in slices:
        s.SliceThickness = slice_thickness

    # pydicom.dcmread()
        
    return slices

def get_pixels_hu(scans):
    image = np.stack([s.pixel_array for s in scans])
    # Convert to int16 (from sometimes int16), 
    # should be possible as values should always be low enough (<32k)
    image = image.astype(np.int16)

    # Set outside-of-scan pixels to 1
    # The intercept is usually -1024, so air is approximately 0
    image[image == -2000] = 0
    
    # Convert to Hounsfield units (HU)
    intercept = scans[0].RescaleIntercept
    slope = scans[0].RescaleSlope
    
    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)
        
    image += np.int16(intercept)
    
    return np.array(image, dtype=np.int16)

id=0
patient = load_scan(data_path)
print("Finished Loading")
# print(patient)
print("Grabbing Pixels")
imgs = get_pixels_hu(patient)
print("Finished Grabbing Pixels")
np.save(output_path + "fullimages_%d.npy" % (id), imgs)

file_used=output_path+"fullimages_%d.npy" % id
imgs_to_process = np.load(file_used).astype(np.float64) 

plt.hist(imgs_to_process.flatten(), bins=50, color='c')
plt.xlabel("Hounsfield Units (HU)")
plt.ylabel("Frequency")
plt.show()

id = 0
imgs_to_process = np.load(output_path+'fullimages_{}.npy'.format(id))

def sample_stack(stack, rows=6, cols=6, start_with=10, show_every=3):
    fig,ax = plt.subplots(rows,cols,figsize=[12,12])
    for i in range(rows*cols):
        ind = start_with + i*show_every
        ax[int(i/rows),int(i % rows)].set_title('slice %d' % ind)
        ax[int(i/rows),int(i % rows)].imshow(stack[ind],cmap='gray')
        ax[int(i/rows),int(i % rows)].axis('off')
    plt.show()

sample_stack(imgs_to_process)

print ("Slice Thickness: %f" % patient[0].SliceThickness)
print ("Pixel Spacing (row, col): (%f, %f) " % (patient[0].PixelSpacing[0], patient[0].PixelSpacing[1]))

id = 0
imgs_to_process = np.load(output_path+'fullimages_{}.npy'.format(id))
def resample(image, scan, new_spacing=[1,1,1]):
    # Determine current pixel spacing
    print(scan[0].SliceThickness)
    print(scan[0].PixelSpacing)

    # spacing = map(float(), ([scan[0].SliceThickness] + scan[0].PixelSpacing))
    spacing = [scan[0].SliceThickness + float(scan[0].PixelSpacing[0]), 
                        scan[0].SliceThickness + float(scan[0].PixelSpacing[1])
                        ,scan[0].SliceThickness + float(scan[0].PixelSpacing[1])]
    spacing = np.array(list(spacing))

    print(spacing)

    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor
    
    print("creating image")
    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor)
    print("done image")
    return image, new_spacing

# print ("Shape before resampling\t", imgs_to_process.shape)
# imgs_after_resamp, spacing = resample(imgs_to_process, patient, [1,1,1])
# print ("Shape after resampling\t", imgs_after_resamp.shape)

def make_mesh(image, threshold=-300, step_size=1):

    print ("Transposing surface")
    p = image.transpose(2,1,0)
    
    print ("Calculating surface")
    verts, faces, norm, val = measure.marching_cubes_lewiner(p, threshold, step_size=step_size, allow_degenerate=True)
    # verts, faces, norm, val = measure.marching_cubes_classic()
    return verts, faces

def plotly_3d(verts, faces):
    x,y,z = zip(*verts) 
    
    print ("Drawing")
    
    # Make the colormap single color since the axes are positional not intensity. 
#    colormap=['rgb(255,105,180)','rgb(255,255,51)','rgb(0,191,255)']
    colormap=['rgb(236, 236, 212)','rgb(236, 236, 212)']
    
    fig = FF.create_trisurf(x=x,
                        y=y, 
                        z=z, 
                        plot_edges=False,
                        colormap=colormap,
                        simplices=faces,
                        backgroundcolor='rgb(64, 64, 64)',
                        title="Interactive Visualization")
    iplot(fig)

def plt_3d(verts, faces):
    print ("Drawing")
    x,y,z = zip(*verts) 
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Fancy indexing: `verts[faces]` to generate a collection of triangles
    mesh = Poly3DCollection(verts[faces], linewidths=0.05, alpha=1)
    face_color = [1, 1, 0.9]
    mesh.set_facecolor(face_color)
    ax.add_collection3d(mesh)

    ax.set_xlim(0, max(x))
    ax.set_ylim(0, max(y))
    ax.set_zlim(0, max(z))
    ax.set_facecolor((0.7, 0.7, 0.7))
    plt.show()

print("Creating Mesh")
v, f = make_mesh(imgs_to_process, 350)
print(v)
# print(v.shape())
print(f)
# print(f.shape())
np.save("C:/Users/legom/Documents/GitHub/3DMeasure/data/PRICT-28/Scan_Verts",v)
np.save("C:/Users/legom/Documents/GitHub/3DMeasure/data/PRICT-28/Scan_Faces",f)
# file = open("C:/Users/legom/Documents/GitHub/3DMeasure/data/PRICT-28/Scan_Faces.txt", "w")
# file.write(v)
# file.close()
# file = open("C:/Users/legom/Documents/GitHub/3DMeasure/data/PRICT-28/Scan_Faces.txt", "w")
# file.write(f)
# file.close()

# plt_3d(v, f)
