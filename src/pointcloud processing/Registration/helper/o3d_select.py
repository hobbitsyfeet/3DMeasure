import open3d as o3d

def pick_points(o3d_cloud):
    """
    """
    print("")
    print(
        "1) Please pick at least three correspondences using [shift + left click]"
    )
    print("   Press [shift + right click] to undo point picking")
    print("2) Afther picking points, press q for close the window")
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(o3d_cloud)
    vis.run()  # user picks points
    vis.destroy_window()
    print("")
    #returns the inices of the users picked points
    return vis.get_picked_points()