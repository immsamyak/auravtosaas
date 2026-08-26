# Local VTO Testing Guide (Windows 10/11)

Testing heavy AI models like **MobileVTON** and diffusion networks on a Windows laptop with a **GTX 1050** requires some careful configuration. The GTX 1050 is an older GPU with limited VRAM (typically 2GB to 4GB), which means we have to aggressively optimize memory usage or fall back to your CPU (which you have plenty of RAM for).

Here is the exact step-by-step process to set up your secondary Windows laptop for testing these AI models locally.

---

## Step 1: Install Prerequisites

1. **Install Python**: Ensure you have Python 3.10, 3.11, or 3.12 installed on Windows. Make sure to check "Add Python to PATH" during installation.
2. **Install Git**: Download and install [Git for Windows](https://git-scm.com/download/win).
3. **Update GPU Drivers**: Ensure your Nvidia GTX 1050 drivers are fully updated via GeForce Experience.

## Step 2: Clone the Project and Set Up the Virtual Environment

Open **Command Prompt (cmd)** or **PowerShell** and run:

```cmd
git clone https://github.com/immsamyak/auravtosaas.git
cd auravtosaas/backend

# Create a fresh Python virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

## Step 3: Install PyTorch with CUDA Support

Since you have an Nvidia GPU, you *must* install the specific version of PyTorch that can communicate with your GTX 1050 (CUDA). 

Run this exact command to install PyTorch for Windows:
```cmd
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## Step 4: Install AI Dependencies

Next, install the specific Machine Learning libraries required by `mobile_vton.py`:

```cmd
pip install diffusers transformers accelerate huggingface_hub pillow numpy
```

## Step 5: Handling the GTX 1050 Bottleneck (Crucial!)

> [!WARNING]
> **VRAM Limitations**
> The MobileVTON engine relies on diffusion models (UNets, VAEs, Text Encoders). These usually require 8GB+ of Video RAM. Your GTX 1050 only has 2GB-4GB. If you run it normally, you will instantly get a `CUDA Out Of Memory (OOM)` error.

To test the model on your laptop, you have two choices for your test scripts:

### Option A: CPU Offloading (Slow but uses GPU)
You must cast the models to `float16` and use HuggingFace Accelerate to swap memory between your 20GB of RAM and your GPU.

When initializing pipelines in your testing scripts, ensure `enable_model_cpu_offload()` is called:
```python
import torch
from diffusers import DiffusionPipeline

# Load model in fp16 to save memory
pipeline = DiffusionPipeline.from_pretrained(
    "Mobile_VTON_Model_Path", 
    torch_dtype=torch.float16
)
# This forces layers to move to the GPU only exactly when they are needed, 
# preventing the GTX 1050 from crashing.
pipeline.enable_model_cpu_offload() 
```

### Option B: Pure CPU Mode (Very Slow, but 100% reliable)
Because you have a solid i5 8th Gen CPU and 20GB of RAM, you can bypass the GPU entirely. It might take 1-3 minutes to generate a single image, but it won't crash.

```python
pipeline = DiffusionPipeline.from_pretrained("Mobile_VTON_Model_Path")
pipeline.to("cpu") # Force the model to use your i5 processor
```

## Step 6: Create a Local Test Script

Create a new file in your backend folder called `test_vto_local.py`. You can use this template to test the engine without booting up the entire Django server:

```python
# test_vto_local.py
import sys
import os
import torch
from PIL import Image

# Import the engine directly
from apps.fitting.engines.mobile_vton import MobileVTONEngine

def test_local_vton():
    print("Initializing Mobile VTON Engine...")
    
    # Initialize engine
    engine = MobileVTONEngine()
    
    # Load test images (you will need to put two images in this folder)
    person_image = Image.open("test_person.jpg")
    garment_image = Image.open("test_garment.jpg")
    
    print("Generating Virtual Try-On... (This may take several minutes on an i5/GTX 1050)")
    
    # Run inference
    result_image = engine.generate(
        person_image=person_image,
        garment_image=garment_image,
        garment_type="upper_body" # or lower_body / dresses
    )
    
    result_image.save("vton_output.jpg")
    print("Success! Saved as vton_output.jpg")

if __name__ == "__main__":
    test_local_vton()
```

Run it via:
```cmd
python test_vto_local.py
```

## Summary Checklist
1. ✅ Pull repo on Windows.
2. ✅ Install PyTorch specifically for CUDA (`cu121`).
3. ✅ Install Diffusers and Transformers.
4. ✅ Test using a standalone Python script to bypass the web server logic.
5. ⚠️ Be prepared for slow generations (1-5 minutes per image) due to the GTX 1050's hardware constraints.
