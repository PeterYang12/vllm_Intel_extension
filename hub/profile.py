import os
import yaml
import logging
from typing import Mapping
from hub.utils import error_and_exit
from hub.hardware_inspect import HWSystem

CWD = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CWD)
default_manifest_dir = os.path.join(PROJECT_ROOT, 'configs')
default_manifest_path = os.path.join(default_manifest_dir, 'model_manifests.yaml')
logger = logging.getLogger(__name__)


# TODO
def get_manifest_path() -> str|None:
    if os.path.exists(default_manifest_path):
        logger.info(f"Found manifest file at {default_manifest_path}")
        return default_manifest_path
    else:
        logger.error(f"Manifest file not found at {default_manifest_path}")
    return None


# TODO
def get_all_profiles(manifest_path: str):
    # get all the profiles from the manifest
    with open(manifest_path, 'r') as file:
        manifests = yaml.load(file, Loader=yaml.FullLoader)
    return manifests


def filter_manifest_configs(manifest_path: str):
    # filter out the configs that are suitable for the current system
    manifests = get_all_profiles(manifest_path)
    if len(manifests) > 0:
        logger.info(f"Found {len(manifests)} profiles in the manifest file")
        return manifests
    else:
        logger.error(f"No config found in manifest file {manifest_path}")
        return None


def get_profile_description(profile):
    tags = profile["tags"]
    components = []
    if "hpu" in tags:
        components.append(tags["hpu"])
    if "llm_engine" in tags:
        components.append(tags["llm_engine"])
    if "precision" in tags:
        components.append(tags["precision"])
    if "tp" in tags:
        components.append(f"tp{tags['tp']}")
    if "profile" in tags:
        components.append(tags['profile'])
    return "-".join(components).lower()


# TODO
def get_optimal_manifest_config(
        manifest_path: str, system: HWSystem, override: bool = False
) -> str:
    config_results = filter_manifest_configs(manifest_path)
    if len(config_results) == 0:
        error_message = "No suitable config found in the manifest file"
        # TODO print the detected system configuration
        error_and_exit(error_message)
    else:
        cnt = 0
        choosen_profile_name = None
        for profile_name, profile in config_results.items():
            if cnt == 0:
                choosen_profile_name = profile_name
            profile_description = get_profile_description(profile)
            logger.info(f"Profile {cnt}: {profile_description}")
            cnt += 1
    # TODO
    return choosen_profile_name + ".yaml"


def generate_launch_args_from_profile(optimal_profile_path: str):
    with open(optimal_profile_path, 'r') as file:
        profile_args = yaml.load(file, Loader=yaml.FullLoader)
    backend = profile_args["backend"]
    if profile_args[backend]:
        # TODO
        pass
    else:
        error_message = "Wrong configs in the profile file"
        error_and_exit(error_message)


def generate_profile_args(system: HWSystem):
    manifest_path = get_manifest_path()
    override = False
    if manifest_path is not None:
        optimal_config_profile_name = get_optimal_manifest_config(manifest_path, system, override)
        optimal_config_profile_path = os.path.join(default_manifest_dir, optimal_config_profile_name)
        if os.path.exists(optimal_config_profile_path):
            logger.info(f" The choosen optimal profile path: \n{optimal_config_profile_path}")
            generate_launch_args_from_profile(optimal_config_profile_path)
        else:
            error_message = f"Can't find the optimal profile file. The file path doesn't exist.\n{optimal_config_profile_path}"
            error_and_exit(error_message)
    else:
        error_message = "Can't find the manifest file"
        error_and_exit(error_message)