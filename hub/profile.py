import os
import logging
import yaml
from hub.utils import error_and_exit, check_dir_exist
from hub.hardware_inspect import HWSystem

CWD = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CWD)
default_manifest_dir = os.path.join(PROJECT_ROOT, 'configs')
default_manifest_path = os.path.join(default_manifest_dir, 'model_manifests.yaml')
logger = logging.getLogger(__name__)


def get_manifest_path() -> str|None:
    """Get the manifest file path"""
    if os.path.exists(default_manifest_path):
        logger.info("Found manifest file at %s", default_manifest_path)
        return default_manifest_path

    logger.error("Manifest file not found at %s", default_manifest_path)
    return None


def get_all_profiles(manifest_path: str):
    """Get all the profiles from the manifest"""
    with open(manifest_path, 'r', encoding="utf-8") as file:
        manifests = yaml.load(file, Loader=yaml.FullLoader)
    return manifests


def filter_manifest_configs(manifest_path: str):
    """Filter out the configs that are suitable for the current system"""
    manifests = get_all_profiles(manifest_path)
    if len(manifests) > 0:
        logger.info("Found %s profiles in the manifest file", len(manifests))
        return manifests
    else:
        logger.error("No config found in manifest file %s", manifest_path)
        return None


def get_profile_description(profile):
    """Get the description of the profile"""
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


def get_optimal_manifest_config(
        manifest_path: str, system: HWSystem, override: bool = False
) -> str:
    """Get the optimal config from the manifest"""
    config_results = filter_manifest_configs(manifest_path)
    choosen_profile_name = ""
    if len(config_results) == 0:
        error_message = "No suitable config found in the manifest file"
        # TODO: print the detected system configuration
        error_and_exit(error_message)
    else:
        cnt = 0
        for profile_name, profile in config_results.items():
            if cnt == 0:
                choosen_profile_name = profile_name
            profile_description = get_profile_description(profile)
            logger.info("Profile %s: %s", cnt, profile_description)
            cnt += 1

    return choosen_profile_name + ".yaml"


def generate_launch_args_from_profile(optimal_profile_path: str) -> dict:
    """Generate the launch arguments from the optimal profile"""
    with open(optimal_profile_path, 'r', encoding="utf-8") as file:
        profile_args = yaml.load(file, Loader=yaml.FullLoader)
    backend = profile_args["backend"]
    config_args = {}
    if profile_args[backend]:
        # dump the args into a dict
        config_args.update(profile_args[backend])
        return config_args
    else:
        error_message = "Wrong configs in the profile file"
        error_and_exit(error_message)


def dump_config_args_to_yaml(config_args: dict, output_path: str, filename: str = "config.yaml"):
    """Dump the config args into a yaml file"""
    if check_dir_exist(output_path):
        output_file_path = os.path.join(output_path, filename)
        with open(output_file_path, 'w', encoding="utf-8") as file:
            yaml.dump(config_args, file)
        logger.info("Dumped the config args into %s", output_file_path)


def generate_profile_args(system: HWSystem) -> dict:
    """Generate the launch arguments from the optimal profile"""
    manifest_path = get_manifest_path()
    override = False
    if manifest_path is not None:
        optimal_config_profile_name = get_optimal_manifest_config(manifest_path, system, override)
        optimal_config_profile_path = os.path.join(
            default_manifest_dir, optimal_config_profile_name)
        if os.path.exists(optimal_config_profile_path):
            logger.info(" The choosen optimal profile path: %s", optimal_config_profile_path)
            config_args = generate_launch_args_from_profile(optimal_config_profile_path)
            if config_args:
                return config_args
            else:
                error_message = "Wrong configs in the profile file"
                error_and_exit(error_message)
        else:
            error_message = (
                f"Can't find the optimal profile file. The file path: "
                f"'{optimal_config_profile_path}' doesn't exist."
                )
            error_and_exit(error_message)
    else:
        error_message = "Can't find the manifest file"
        error_and_exit(error_message)
