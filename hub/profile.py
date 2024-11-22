import os
import yaml
import logging
from pathlib import Path

CWD = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CWD)
default_manifest_path = os.path.join(PROJECT_ROOT, 'configs', 'model_manifests.yaml')

# TODO
def get_manifest_path():
    if os.path.exists(default_manifest_path):
        return default_manifest_path
    else:
        logging.error(f"Manifest file not found at {default_manifest_path}")
    return None


# TODO
def get_optimal_manifest_config(
        manifest_path: Path, override: bool = False):
    pass


def get_profile_description():
    pass


def generate_profile_args():
    manifest_path = get_manifest_path()
    override = False
    if manifest_path is not None:
        get_optimal_manifest_config(manifest_path, override)

    else:
        pass
