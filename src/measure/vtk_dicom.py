import vtk
from vtk.util import numpy_support
import numpy
import os

def view_dicom(PathDicom):

    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(PathDicom)
    reader.Update()

    # Load dimensions using `GetDataExtent`
    _extent = reader.GetDataExtent()
    ConstPixelDims = [_extent[1]-_extent[0]+1, _extent[3]-_extent[2]+1, _extent[5]-_extent[4]+1]

    # Load spacing values
    ConstPixelSpacing = reader.GetPixelSpacing()

    # Get the 'vtkImageData' object from the reader
    imageData = reader.GetOutput()
    # Get the 'vtkPointData' object from the 'vtkImageData' object
    pointData = imageData.GetPointData()
    # Ensure that only one array exists within the 'vtkPointData' object
    assert (pointData.GetNumberOfArrays()==1)
    # Get the `vtkArray` (or whatever derived type) which is needed for the `numpy_support.vtk_to_numpy` function
    arrayData = pointData.GetArray(0)

    # Convert the `vtkArray` to a NumPy array
    ArrayDicom = numpy_support.vtk_to_numpy(arrayData)
    # Reshape the NumPy array to 3D using 'ConstPixelDims' as a 'shape'
    ArrayDicom = ArrayDicom.reshape(ConstPixelDims, order='F')

def view_dicom_2(PathDicom):
    print("Reading DICOM...")
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(PathDicom)
    reader.Update()
    print("Done Reading.")

    print("Processing Images...")
    imageData = reader.GetOutput()

    volumeMapper = vtk.vtkSmartVolumeMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        volumeMapper.SetInputConnection(imageData.GetProducerPort())
    else:
        volumeMapper.SetInputData(imageData)

    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.ShadeOff()
    volumeProperty.SetInterpolationType(vtk.VTK_LINEAR_INTERPOLATION)

    compositeOpacity = vtk.vtkPiecewiseFunction()
    compositeOpacity.AddPoint(0.0,0.0)
    compositeOpacity.AddPoint(80.0,1.0)
    compositeOpacity.AddPoint(80.1,0.0)
    compositeOpacity.AddPoint(255.0,0.0)
    volumeProperty.SetScalarOpacity(compositeOpacity)

    color = vtk.vtkColorTransferFunction()
    color.AddRGBPoint(0.0  ,0.0,0.0,1.0)
    color.AddRGBPoint(80.0  ,1.0,0.0,0.0)
    color.AddRGBPoint(255.0,1.0,1.0,1.0)
    volumeProperty.SetColor(color)

    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    print("Done Processing.")

    print("Starting VTK...")
    renWin = vtk.vtkRenderWindow();
    ren1 = vtk.vtkRenderer();
    ren1.SetBackground(0, 0, 0);

    renWin.AddRenderer(ren1);
    renWin.SetSize(800, 800);

    iren = vtk.vtkRenderWindowInteractor();
    iren.SetRenderWindow(renWin);


    ren1.AddViewProp(volume)
    ren1.ResetCamera()
    print("Rendering...")
    # Render composite. In default mode. For coverage.
    renWin.Render()

    # 3D texture mode. For coverage.
    # volumeMapper.SetRequestedRenderModeToRayCastAndTexture()
    # renWin.Render()

    # Software mode, for coverage. It also makes sure we will get the same
    # regression image on all platforms.
    # volumeMapper.SetRequestedRenderModeToRayCast()
    # renWin.Render()

    print("Displaying...")
    iren.Start()

if __name__ == "__main__":
        
    PathDicom = "C:/Users/legom/Documents/GitHub/3DMeasure/data/PRICT-28/series_7/"
    # view_dicom(PathDicom)
    view_dicom_2(PathDicom)