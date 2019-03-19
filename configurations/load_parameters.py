import yaml


def load_parameters(config_file_path):
    """
    Load parameters defined in a .yml configuration file into a dictionary
    """
    with open(config_file_path) as f:
        parameters = yaml.safe_load(f)

    return parameters
