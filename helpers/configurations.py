import os
import json
from typing import Dict


def get_config(config: str) -> Dict[str, object]:
    """
    Returns the configuration for the algorithm based on the config passed,
    read from the JSON file.
    """
    if os.path.isfile(config):
        # Read configuration
        with open(config) as config_file:
            configuration = json.load(config_file)
        return configuration
    else:
        exit("Config file not found")
