import os

from mspypeline import MSPInitializer, UIHandler, MaxQuantPlotter


def experiment_design_location(experimental_design):
    script_loc = os.path.dirname(os.path.realpath(__file__))
    path_mock_data = os.path.join(script_loc, "mock_data")
    return os.path.join(path_mock_data, experimental_design)


# TODO test case with no pathways and go terms
def test_all_designs_raw():
    configs = {
        "global_settings": {
            "save_path": None
        },
        "plot_r_volcano_settings": {
            "create_plot": False
        },
        "plot_pathway_timeline_settings": {
            "create_plot": False
        },
        "plot_venn_groups_settings": {
            "create_plot": False
        },
        "plot_venn_results_settings": {
            "create_plot": False
        }
    }
    # configs = {"pathways": ["A", "B"]}
    # configs = {"go_terms": ["A", "B"]}
    # set all intensites to log2
    for experiment_design in ("has_group_has_tech", ):  # "has_group_no_tech", "no_group_has_tech", "no_group_no_tech"
        if "has_group" in experiment_design:
            configs["has_group"] = True
        else:
            configs["has_group"] = False
        if "has_tech" in experiment_design:
            configs["has_replicates"] = True
        else:
            configs["has_replicates"] = False
        target_dir = experiment_design_location(experiment_design)
        # UIHandler(target_dir, configs=configs)
        mspinit = MSPInitializer(target_dir, "default")
        mspinit.init_config()
        mspinit.configs.update(configs)
        mspinit.read_data()
        # create plotter from initializer
        for key in mspinit.configs.keys():
            if "settings" in key:
                mspinit.configs[key]["levels"] = [1, 2]
        mspplots = MaxQuantPlotter.from_MSPInitializer(mspinit)
        # create all plots and other results
        mspplots.create_results()
        # for file in os.listdir(target_dir):
        #     if file == "config" or file == "txt":
        #         continue
        #     else:
        #         os.rename(os.path.join(target_dir, file), os.path.join(target_dir, file + "_raw"))
