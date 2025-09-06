[HunyuanVideo-Foley](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley)
The goal of this project is to take an existing project that already works on its own and containerize it to work on Runpod.  Everything should be installed at RUNTIME after the container has started.  This is critical to understand, and must be followed.

**Rules to always follow**

 1. This will run in a container on Runpod, so never install dependencies, or modules on the local server.  Do not forget the #1 rules.
 2. Do not build the container on this server.  It will be built on github, and deployed to dockerhub.
 3. The docker-compose command has been deprecated it is now 'docker compose'
 4. Never expose secrets or keys to to github, always use dummy spaceholders instead.
 
 **MCP servers to use**
 
 1. as context7 for documentation when necessary as it will have up to date information.
 2. ask serena for memories to get context about the project.  conversely when you have made significant changes, ask serena to write a memory documenting the changes for future developers and sessions.
 3. ask fetch to get web pages when you need to get context from the internet.

**Github information**
- The upstream github project is https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley.git .  The repository we will be working on is https://github.com/sruckh/HunyuanVideo-Foley-Runpod .  All changes will be pushed to the sruckh/OmniTry-Runpod repository.
- two github secrets have been configured:  DOCKER_USERNAME and DOCKER_PASSWORD.  These should be used for pushing container image to Dockerhub

**Dockerhub**
- The dockerhub repository for this container is gemneye/

**Github action**
- If it has not already been completed set up the github action to automatically build and push the container to dockerhub.  Also create a description for the container that users can see on dockerhub.

**Environmental Variables**
- Any environmental variables that are necessary will be configured on Runpod.

**How to install -- This is ONLY for AMD64 system do not setup this up for any other architecture**

 1. Start with the base image nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04
 
**Everything from here happens at Runtime after container has started**
- ask context 7 how to install and use hf (not huggingface-cli).  make sure hf get installed correctly for later steps.

 1. Install pytorch: pip3 install torch torchvision
 2. clone repository: git clone https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley
 3. cd HunyuanVideo-Foley
 4. pip install -r requirements.txt
 5. git clone https://huggingface.co/tencent/HunyuanVideo-Foley
 6. Use hf to download: tencent/HunyuanVideo-Foley
 7. export HIFI_FOLEY_MODEL_PATH=PRETRAINED_MODEL_PATH_DIR ;where PRETRAINED_MODEL_PATH_DIR is the path where models were downloaded.
 8. install flash_attn:  https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.8cxx11abiFALSE-cp310-cp310-linux_x86_64.whl
 9. Launch the gradio app:  python3 gradio_app.py


