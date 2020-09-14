# Normalize Pose

Normalize pose leverages the parsed information to retain the form of each part as best as possible. This means the model was segmented at each of the joints, including the joints such that each part should be somwhat static no matter the given position.

This is useful since deep learning models can learn to segment this type of information automatically. If so, a dynamic model, if segmented properly, can use rigid registration techniques to register a whole model. We can see this by using the StickMan captured with Kinect Azure.

#### Source Pose and Target Pose
<img src="/docs/photos/Source_Pose.jpg" width="324" height="324"><img src="/docs/photos/Target_Pose.jpg" width="324" height="324">
#### Result Pose (white)
<img src="/docs/photos/Pose_Registration_Result.jpg" width="324" height="324">

