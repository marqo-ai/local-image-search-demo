
# Marqo E-Commerce Local Search Demo

This is an image search demo that uses Marqo to do multimodel search with weighted queries. The entire program is designed to run locally using the Marqo docker image on your own machine. All data is provided by Marqo via S3 and will be automatically indexed when you run the app. The model used for the application is ```open_clip/ViT-B-32/laion2b_s34b_b79k```, but Marqo can also support hundreds of other open source embedding models, see: https://docs.marqo.ai/2.0.0/Guides/Models-Reference/dense_retrieval/

__NOTE: By default this application starts with 10,000 images which means that there may not be relevant results for all searches. The images you get are randomised.__ (Edit `.env.local` to add more images).

<p align="center">
  <img src="readme_assets/shirt1.gif"/>
</p>

# Index

- [Marqo E-Commerce Local Search Demo](#marqo-e-commerce-local-search-demo)
- [Index](#index)
- [Running Marqo](#running-marqo)
    - [Running on CPU](#running-on-cpu)
    - [Running on GPU](#running-on-gpu)
- [Dependencies](#dependencies)
    - [Make virutal environment](#make-virutal-environment)
    - [Activate the virtual environment](#activate-the-virtual-environment)
    - [Install requirements](#install-requirements)
- [Running the Application](#running-the-application)
- [Re-Indexing Data](#re-indexing-data)

# Running Marqo

The steps and command for different devices are provided below.

### Running on CPU
```
docker run --name marqo -p 8882:8882 marqoai/marqo:2.0.0
```
### Running on GPU

Currently, only CUDA capable (Nvidia) GPU's are supported. For instructions on running on GPU with AWS, the following guide will help you configure the correct AMI. https://docs.marqo.ai/latest/Guides/using_marqo_with_a_gpu/. Note that if you're running on AWS, using the AMI is highly recommended as opposed to installing the toolkit manually.

Alternatively, you can follow the below instructions:

1. Install NVIDIA Container Toolkit.
2. Add a `--gpus all` flag to the Docker run command. Note that this flag should appear after the run command but before the end.

Install NVIDIA Container Toolkit which is required for the GPU to work with Docker. For more detail refer to [the original instructions](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).

Once NVIDIA Container Toolkit is installed, you can run Marqo with `--gpus all`:
```
docker run --name --gpus all marqo -p 8882:8882 marqoai/marqo:2.0.0
```
# Dependencies
Install the dependencies in a virtual environment.

### Make virutal environment
```
python -m venv venv
```
### Activate the virtual environment

Windows:
```
.\venv\Scripts\activate
```
Linux/Mac:
```
source venv/bin/activate
```
### Install requirements
```
pip install -r requirements.txt
```

# Running the Application

Before you run the application you may want to configure the environment variable to suite your system. There are two that are used:
```
N_DOCUMENTS=<number of documents to use in the index, removing the will use all documents>
MARQO_INDEX_NAME=<the name of the index to create and use, the default should be fine>
```

If you are on CPU then a high N_DOCUMENTS may take hours to index.

Index the data:
```
python3 index_data.py
```

Run the server (Note: search may be slow if indexing is still running - especially on a CPU):
```
python3 app.py
```

(This will first check if the index exists on your machine. If it doesn't then it will be automatically created using `N_DOCUMENTS` documents.)
