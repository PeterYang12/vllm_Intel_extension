#/usr/env/bin bash
set -e

echo "==============================="
echo "Starting the extension"
cd /workspace/vllm_Intel_extension/
python -m entrypoints.api_extension

echo "==============================="
echo "Starting the server"
python3 -m vllm.entrypoints.openai.api_server --conf /workspace/vllm_Intel_extension/temp/config.yaml