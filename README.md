# vllm_Intel_extension

Intel extension for vllm

## Getting Started

### Installation

#### build docker image

```bash
docker build --no-cache --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy -f Dockerfile.hpu -t llama3.1-8b-instruct-test .
```

#### to run

```bash
docker run -it --rm --runtime=habana -e VLLM_SKIP_WARMUP=true -v ~/.cache/huggingface:/root/.cache/huggingface -p 8000:8000 -e HF_TOKEN=${HF_TOKEN} -e HABANA_VISIBLE_DEVICES="0" -e OMPI_MCA_btl_vader_single_copy_mechanism=none --cap-add=sys_nice  --ipc=host  llama3.1-8b-instruct-test
```

#### For develop

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### To run

```bash
python -m entrypoints.api_extension
```
