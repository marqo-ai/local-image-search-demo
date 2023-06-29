
# Marqo E-Commerce Local Search Demo

This is an image search demo that uses Marqo to do multimodel search with weighted queries. The entire program is designed to run locally using the Marqo docker image on your own machine. All data is provided by Marqo via S3 and will be automatically indexed when you run the app.

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
    - [Running on M1 or M2](#running-on-m1-or-m2)
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
docker pull marqoai/marqo:latest
docker rm -f marqo
docker run --name marqo -it --privileged -p 8882:8882 --add-host host.docker.internal:host-gateway marqoai/marqo:latest
```
### Running on GPU

Currently, only CUDA capable (Nvidia) GPU's are supported. If you have a GPU on the host machine and want to use it with Marqo, there are two things to do:

1. Install nvidia-docker2.
2. Add a --gpus all flag to the Docker run command. Note that this flag should appear after the run command but before the end.

Install nvidia-docker2 which is required for the GPU to work with Docker. Steps for an Ubuntu machine are provided below. For more detail refer to [the original instructions](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).
```
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
```
Once nvidia-docker2 is installed, you can run Marqo with `--gpus all`:
```
docker run --name marqo --gpus all --privileged -p 8882:8882 --add-host host.docker.internal:host-gateway marqoai/marqo:latest
```

### Running on M1 or M2

In one terminal run:
```
docker rm -f marqo-os; docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" marqoai/marqo-os:0.0.3-arm
```
Once that is done, open another terminal and run:
```
docker rm -f marqo; docker run --name marqo --privileged \
    -p 8882:8882 --add-host host.docker.internal:host-gateway \
    -e "OPENSEARCH_URL=https://localhost:9200" \
    marqoai/marqo:latest
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

Before you run the application you may want to configure the environment variable to suite your system. There are three that are used:
```
N_DOCUMENTS=<number of documents to use in the index, removing the will use all documents>
MARQO_DEVICE=<the device to use for Marqo, must be cpu or cuda>
MARQO_INDEX_NAME=<the name of the index to create and use, the default should be fine>
```

If you are on CPU then a high N_DOCUMENTS may take hours to index.

Run the server:
```
python3 app.py
```

This will first check if the index exists on your machine. If it doesn't then it will be automatically created using `N_DOCUMENTS` documents.

# Re-Indexing Data
If you wish to index the data again you can run the index_data script directly. If the index already exists then you will be prompted incase you want to replace it.
```
python3 index_data.py
```