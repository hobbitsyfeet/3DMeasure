# Depth Cameras

### Kinect Azure and Realsense D415
<img src ="docs/DepthCameras/Distance(Kinect).PNG" width="500" height="300">
<img src = "docs/DepthCameras/Distance(Realsense).jpg"  width="500" height="300">

These results show the range a camera can capture a taxidermy raccoon arm (2cm width) at different ranges. Time of day and location vary. Both outdoors. Kinect was during dusk, while realsense was in the shade of the building. 

The falloff is in different directions due to:

1) The depth pixel location being blended with the background (a longer measurment).
2) Depth pixel was N/A, so the choice was to capture the pixel closest to the wrist, even if it was not the wrist (A shorter measurment).

This demonstrates the flaws and tradeoffs between the two cameras.

Measurment "Ground Truths" differ between camera studies, as the estimated locations was measured before each study, and those locations were set to be the targets to measure. This gives about 0.5cm (5mm) difference, which was determined to be a reasonable degree of error.
