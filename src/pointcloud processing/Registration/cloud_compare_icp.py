import subprocess
import os
import argparse
from helper import load
import ntpath
import os.path

#### GLOBAL ####
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--cc_dir', default="F:/CloudCompare/", help='The location of CloudCompare install directory C:/CloudCompare')
args = parser.parse_args()

cloud_compare_dir = args.cc_dir


def cc_icp(source_dir, target_dir, output_dir):
    """
    This implements and executes ICP from command line using Cloud Compare
    https://www.danielgm.net/cc/

    Download from: http://www.danielgm.net/cc/release/

    set cc_dir using --cc_dir <CLOUD_COMPARE_PATH> when executing.
    """

    head, source_tail = ntpath.split(source_dir)

    #Warning: must be first if required. 
    silent = " -silent "
    launch_cc = cloud_compare_dir + "CloudCompare"
    open_files =  " -o " + source_dir + " -o " + target_dir
    
    autosave_off = " -AUTO_SAVE OFF "
    compute_normals = " -COMPUTE_NORMALS "
    register_files = " -ICP "

    print(output_dir+source_tail)

    # save_files =  " -NO_TIMESTAMP -SAVE_MESHES"
    # save_formats = "-M_EXPORT_FMT FBX -FBX_EXPORT_FMT FBX_Binary "
    save_formats = "-C_EXPORT_FMT PLY -PLY_EXPORT_FMT ASCII "
    # save_files = " -PLY_EXPORT_FMT ASCII " " -SAVE_CLOUD FILE \"" + source_dir[:-4] + "_REGISTERED.ply " + target_dir[:-4] +"_REGISTERED.ply\""
    command = launch_cc + silent + save_formats + open_files + register_files #+ " -NO_TIMESTAMP "


    with subprocess.Popen(command,
                cwd=cloud_compare_dir,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stdin=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True) as proc:

        proc.communicate(timeout=15)

        # for line in proc.stdout:
        #     #the real code does filtering here
        #     print ("CC:", line.rstrip())

def per_part_registration(source_file_list, target_file_list, output_dir):

    while(target_file_list):
        for file in source_file_list:
            head, source_tail = ntpath.split(file)
            head, target_tail = ntpath.split(target_file_list[0])
            # print("TESTING ",target_filenames[0], "==?",file[1])
            if source_tail == target_tail:
                # print(target_file_list[0])
                # print(file)
                # source_idx = file[0]

                # print("Cloud compare registration!")
                print("ALIGNING ", file, target_file_list[0])
                cc_icp(file, target_file_list[0], output_dir)
                # print("REMOVING ",target_filenames[0])

                del target_file_list[0]
        if target_file_list:
            del target_file_list[0]
        else:
            break

if __name__ == "__main__":


    os.chdir(cloud_compare_dir)

    file_list_source = load.get_files_from_folder()
    file_list_target = load.get_files_from_folder()

    parent = os.path.abspath(os.path.join(file_list_target[0], os.pardir))
    output_path = parent+"_REGISTERED"

    if not os.path.isdir(output_path):
    
        os.mkdir(output_path)
    

    per_part_registration(file_list_source, file_list_target, output_path)
                
    print("Complete")