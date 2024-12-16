import os

# Endpoint defined in hub/api.py
ENDPOINT = "https://api.templatehub.org"

# filename defined in hub/download.py
REPOSITORY_TYPE_MODEL = "model"
REPOSITORY_TYPE_MODEL_URL_PREFIX = "model/"
ONNX_WEIGHTS_FILENAME = "model.onnx"
PYTORCH_WEIGHTS_FILENAME = "model.pth"
TF_WEIGHTS_FILENAME = "model.h5"
TF2_WEIGHTS_FILENAME = "model.tf"
FLAX_WEIGHTS_FILENAME = "model.msgpack"
TORCH_SCRIPT_WEIGHTS_FILENAME = "model.pt"

CONFIG_FILENAME = "config.json"
TOKENIZER_FILENAME = "tokenizer.json"
VOCAB_FILENAME = "vocab.json"
TRAINING_ARGS_FILENAME = "training_args.json"

VERSION_FILE = "version.txt"
METADATA_FILE = "metadata.json"

REPOSITORY_TYPE_DATASETS = "datasets"
REPOSITORY_TYPE_DATASETS_URL_PREFIX = "datasets/"

REPOSITORY_TYPES = [REPOSITORY_TYPE_MODEL, REPOSITORY_TYPE_DATASETS, None]
REPOSITORY_TYPES_URL_PREFIX = [REPOSITORY_TYPE_MODEL_URL_PREFIX, REPOSITORY_TYPE_DATASETS_URL_PREFIX, None]

URL_HOME= "https://api.templatehub.org"