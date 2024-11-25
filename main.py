from hub.profile import generate_profile_args
import logging
from hub.hardware_inspect import get_hardware_spec

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info("Generating profile arguments")
    # TODO: Get the hardware specification
    system = get_hardware_spec()
    generate_profile_args(system)
    # TODO: write the args into a yaml file
    # Then launch the api_server
    # vllm serve SOME_MODEL --config config.yaml
    # https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html#command-line-arguments-for-the-server
    # Note that, python3 -m "vllm.entrypoints.openai.api_server" does not work
    # need extra work or upstream fix 