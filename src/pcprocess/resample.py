import pcl
from load import get_file

if __name__ == "__main__":
    cloud_path, cloud_format = get_file()
    cloud = pcl.load(cloud_path, format=cloud_format)
    for i in range(1,20):
        
        tree = cloud.make_kdtree()

        #create moving least squares settings
        mls = cloud.make_moving_least_squares()
        mls.set_Compute_Normals(True)
        mls.set_polynomial_fit(True)
        mls.set_Search_Method(tree)
        print(str(0.01 * i))
        mls.set_search_radius(0.01 * i)

        print("Processing MLS...")
        mls_points = mls.process()
        print("Finished Processing MLS")
        print(mls_points)
        output = "MLS_0-" + str(i) + ".pcd"
        pcl.save_PointNormal(mls_points, output)