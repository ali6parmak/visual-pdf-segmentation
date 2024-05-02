<h2 align="center">Visual PDF Segmentation</h3>
<p align="center">A service for extracting useful information from PDF files.</p>

---

## Table of Contents

- [Dependencies](#dependencies)
  - [Installing torch](#installing-torch)
  - [Installing detectron2](#installing-detectron2)
- [Getting Started](#getting-started)
- [Usage](#usage)

## Dependencies
- Python >= 3.11
- poppler >= 23.04.0
- torch >= 2.1.1
- detectron2

### Installing torch


If your CUDA drivers properly installed, installing torch should be fairly simple. You can refer to this link: [PyTorch](https://pytorch.org)

For previous versions of torch, refer to this [link](https://pytorch.org/get-started/previous-versions/).
To install torch 2.1.1 with CUDA 11.8, you can use:

```
pip install torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 --index-url https://download.pytorch.org/whl/cu118
```

To check if torch properly installed and CUDA is available:

```
import torch

print(torch.cuda.is_available())
```


### Installing detectron2

Installing detectron2 can be a little bit tricky. Before starting installing it, please ensure that your CUDA drivers are properly set up. Then, please follow these steps in order:

- Run the following commands in terminal (if you have not done it in past). If your Python version is not 3.11, you should change the version in the third command:
```
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11-dev
```

- Install detectron2 via:
```
python -m pip install git+https://github.com/facebookresearch/detectron2.git
```


## Getting Started

Follow these steps to run the project on your local machine.

### Prerequisites

Make sure you have the following installed:

- CUDA drivers (if using GPU acceleration).
- Other dependencies as listed in the [Dependencies](#dependencies) section.

---

1. Clone the repository to your local machine:

```
git clone https://github.com/ali6parmak/visual-pdf-segmentation.git
```

2. Install the required Python packages (If you have already installed the torch, consider commenting it out inside requirements.txt):

```
pip install -r requirements.txt
```

## Usage

Run:
```
python src/segment_pdf.py path/to/pdf.pdf path/to/pdf2.pdf path/to/pdf3.pdf
```


## How to use GPU

To use the GPU in the docker containers

1. Install the package:
        
    nvidia-container-toolkit


2. Restart docker service

    systemctl restart docker



3. Start the service with
    
    make start_gpu