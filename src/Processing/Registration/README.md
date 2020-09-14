# Normalize Pose

Normalize pose leverages the parsed information to retain the form of each part as best as possible. This means the model was segmented at each of the joints, including the joints such that each part should be somwhat static no matter the given position. For this, we use Cloud Compare ICP registration.

This is useful since deep learning models can learn to segment this type of information automatically. If so, a dynamic model, if segmented properly, can use rigid registration techniques to register a whole model. We can see this by using the StickMan captured with Kinect Azure.

#### Source/Target Pose and Target/Result Pose
<img src="/docs/photos/Source_Target.jpg" width="324" height="324"><img src="/docs/photos/Target_Result.jpg" width="324" height="324">

#### How to use:
Run normalize_pose.py `python normalize_pose.py`, the first folder will be the source set, and second folder will be the target set. Two selection windows will display one after the other when selected. The data to test this is supplied in `data/Stickman_Segmented`. 

The output will be marked with the suffix __REGISTERED_ in the source pose folder. 
Note: The visualization shows the Source and Target. The next visualization will show the Target and the Results.
