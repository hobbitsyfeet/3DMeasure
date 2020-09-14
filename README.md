
# 3DMeasure

## Featured Tools
[Per-Part Rigid Registration for Pose Normalization](https://github.com/hobbitsyfeet/3DMeasure/tree/master/src/Processing/Registration#normalize-pose)

## Install PCL
Install Point Cloud Library (WINDOWS). Follow the instructions on the [PCL github page](https://github.com/strawlab/python-pcl).

Install the appropriate PCL 1.8.1 for your system. (Then Restart your computer)

 [Visual Studio 2015 - 32 bit](https://github.com/PointCloudLibrary/pcl/releases/download/pcl-1.8.1/PCL-1.8.1-AllInOne-msvc2015-win32.exe)
 
 [Visual Studio 2017 - 32 bit](https://github.com/PointCloudLibrary/pcl/releases/download/pcl-1.8.1/PCL-1.8.1-AllInOne-msvc2017-win32.exe)
 
 [Visual Studio 2015 - 64 bit](https://github.com/PointCloudLibrary/pcl/releases/download/pcl-1.8.1/PCL-1.8.1-AllInOne-msvc2015-win64.exe)
 
 [Visual Studio 2017 - 64 bit](https://github.com/PointCloudLibrary/pcl/releases/download/pcl-1.8.1/PCL-1.8.1-AllInOne-msvc2017-win64.exe)


### Download the Wheel needed for pip
To get the appropriate pip install, [download the wheel](https://ci.appveyor.com/project/Sirokujira/python-pcl-iju42/history) (the first green and the appropriate version, the download exists under Artifacts)


### Setup Environment

Under User variables for ______, Edit the variable named Path.
Add both OpenNI2 and PCL to the path, it will look similar to this:

        C:\Program Files\OpenNI2\Samples\Bin
        C:\Program Files\PCL 1.8.1\bin

### Pip install the PCL Wheel
After all this is complete, (replacing XXX by the right string)
It will, and MUST look something like this: python_pcl-0.3-cp36-cp36m-win_amd64.whl

    pip install python_pcl-XXX.whl

## Install PyK4a (Kinect Azure)

#### Linux

Make sure your LD_LIBRARY_PATH contains the directory of k4a.lib

`pip install pyk4a`

##### Windows:
 * You can 1.4.1 Windows Installer [Here](https://download.microsoft.com/download/3/d/6/3d6d9e99-a251-4cf3-8c6a-8e108e960b4b/Azure%20Kinect%20SDK%201.4.1.exe),
 Or [Visit the Microsoft Kinect Azure page](https://docs.microsoft.com/en-us/azure/kinect-dk/sensor-sdk-download) for more details.


Follow the instructions mentioned on the [Pyk4a Github Page](https://github.com/etiennedub/pyk4a), as mentioned below:

Make sure you replace the paths in the following instructions with your own k4a sdk path.

`pip install pyk4a --global-option=build_ext --global-option="-IC:\Program Files\Azure Kinect SDK v1.2.0\sdk\include" --global-option="-LC:\Program Files\Azure Kinect SDK v1.2.0\sdk\windows-desktop\amd64\release\lib"`

Don't forget to add the folder containing the release `k4a.dll` to your Path env variable `C:\Program Files\Azure Kinect SDK v1.2.0\sdk\windows-desktop\amd64\release\bin`

# 
# Anaconda

#### SETUP ENVIRONMENTS AS INSTRUCTED ABOVE
You can install it with anaconda though this takes a long time....
Install [anaconda](https://anaconda.org/conda-forge/pcl) and create an environment for python 3.6.

- Once anaconda is installed, link conda to your path in environment variables. 
- Under home search, type "environment variables" and click the Environment Variables... button.
- Under User Variables window, click on the Path and then click the Edit... button. 
- Click New and then add the path where you installed it. By default, it should look something like this. Hit ok, open a terminal window and navigate to the path where you want your project to be. The first allows you to access the command and the seconds allows anaconda to work with your other variables needed.

      C:\Users\username\Anaconda3\condabin
      C:\Users\username\Anaconda3\Scripts
      
      
- You activate the environment with the keyword activate followed by the environment name.

      activate env


Follow these instructions from [conda forge](https://anaconda.org/conda-forge/pcl).
To install this package (point cloud library) with conda run one of the [following](https://gis.stackexchange.com/questions/287773/installing-pcl-module-for-python-3-6-in-anaconda):
  
    conda install -c sirokujira python-pcl --channel conda-forge
    
    
#
# Photos
#
Original Cloud, ground removed (in pipeline)

![Screenshot](https://github.com/hobbitsyfeet/3DMeasure/blob/master/docs/photos/2BearsBeforePipe.PNG)

Clouds clustered and clusters selected

![Screenshot](https://github.com/hobbitsyfeet/3DMeasure/blob/master/docs/photos/2Bears.PNG)

Manual Registration

![Screenshot](https://github.com/hobbitsyfeet/3DMeasure/blob/master/docs/photos/Regerestered_bear.PNG)

Automatic Registration

![Screenshot](https://github.com/hobbitsyfeet/3DMeasure/blob/master/docs/photos/Automatic_registration.PNG)
