# Principal Comonent Analysis (PCA)
PCA has been a very useful tool for dimentionality reduction. In this case, we only collect the vectors of the dimension reduction. 
This results in 3 PCA vectors, where each vector describes one dimension of the object based on it's most significant measures. 
PCA captures the most significant data in PCA1, and less as it goes on. The results of this is 3 perpendicular vectors descibing the object, where each dimension describes the longest, second longest and shortest dimension.

On objects such as Stickman, this shows something significant. Each limb can be easily described by PCA. For limbs and other parts, PCA1 describes length, PCA2 describes Width and PCA3 describes Depth.
Because Depth is not complete given the perspective of the camera, we often can expect this to be the least significant. 

#### PCA1 = Red, PCA2 = Green, PCA3 = Blue.

Notice on the sections that do not contain a "longest" dimension, PCA still describes the object, but there exists no direction like the other parts.

<img src="/docs/photos/Target_Result_PCA.jpg"  width="324" height="324"> <img src="/docs/photos/Target_Result_PCA3.jpg"  width="200" height="324">

##### Notice the usefulness of PCA to determine centroid, and initial directionality for a Global Registration alignment.

PCA was used to try and collect the length of the Raccoon's Right arm. This demonstrates the importance of proper segmentation.

<img src="/docs/photos/Right_Arm_PCA.PNG"  width="500" height="200">
