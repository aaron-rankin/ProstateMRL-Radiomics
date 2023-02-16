import os

def CreateDirs(DataRoot, Norm):
    root_dir = DataRoot + "Aaron\ProstateMRL\Data\Paper1\\"

    if not os.path.exists(root_dir + Norm):
        os.makedirs(root_dir + Norm)

    root_dir = os.path.join(root_dir, Norm)

    # Delta folder
    if not os.path.exists(root_dir + "\\Delta"):
        os.makedirs(root_dir + "\\Delta")

    # Longitudinal folder
    if not os.path.exists(root_dir + "\\Longitudinal"):
        os.makedirs(root_dir + "\\Longitudinal")
        os.makedirs(root_dir + "\\Longitudinal\\DM")
        os.makedirs(root_dir + "\\Longitudinal\\DM\\csvs")
        os.makedirs(root_dir + "\\Longitudinal\\DM\\Figs")
        os.makedirs(root_dir + "\\Longitudinal\\ClusterLabels")
        os.makedirs(root_dir + "\\Longitudinal\\ClusterPlots")

    # Features folder
    if not os.path.exists(root_dir + "\\Features"):
        os.makedirs(root_dir + "\\Features")


