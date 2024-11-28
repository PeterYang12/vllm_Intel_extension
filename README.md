# vllm_Intel_extension

Intel extension for vllm

## Getting Started

### Installation

#### build docker image

```bash
docker build --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy -f Dockerfile.hpu -t test .
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
