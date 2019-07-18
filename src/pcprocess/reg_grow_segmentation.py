import pcl
from load import get_file

def main():
    cloud_path, cloud_format = get_file()
    cloud_path, cloud_format = get_file()
    cloud = pcl.load(cloud_path, cloud_format)

    cloud.make_RegionGrowing()
    


if __name__ == "__main__":
    main()