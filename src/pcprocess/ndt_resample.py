import pcl
import open3d

from load import get_file

if __name__ == "__main__":
    target_path, target_format = get_file()
    target_cloud = pcl.load(target_path)
    open3d.registration.registration_ransac_based_on_feature_matching()
    input_path, input_format = get_file()
    input_cloud = pcl.load(input_path)
    
    ndt = pcl.NormalDistributionsTransform()
    ndt.set_Resolution(1.0)
    ndt.set_StepSize(0.1)

    ndt.set_InputTarget(target_cloud)

    step = ndt.get_StepSize()
    final = ndt.get_FinalNumIteration() 

    
    prob = ndt.get_TransformationProbability()

    ndt.set_InputTarget()
    print(step)
    print(final)
    print(prob)
    