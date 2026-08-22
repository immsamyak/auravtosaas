import psutil
import torch
import time

def check_hardware_for_vton():
    print("--- VTO Hardware Feasibility Test ---")
    
    # 1. System Memory Check
    mem = psutil.virtual_memory()
    total_gb = mem.total / (1024**3)
    available_gb = mem.available / (1024**3)
    print(f"Total System RAM: {total_gb:.2f} GB")
    print(f"Available RAM: {available_gb:.2f} GB")
    
    # Genuine VTO (like CatVTON / StableVITON) requires at least 8GB of pure VRAM/Free RAM
    # just to hold the SD1.5 VAE + CatVTON UNet, and another 4-6GB for the attention maps during forward pass.
    required_gb = 12.0
    print(f"Required Free RAM/VRAM for Diffusion VTO (1024x768): ~{required_gb} GB")
    
    if available_gb < required_gb:
        print("\n[WARNING] Available memory is significantly below the safe threshold for Diffusion VTO.")
        print("Running CatVTON on this system will likely cause severe OS swap, kernel panics, or PyTorch OOM.")
    
    # 2. MPS / CUDA Check
    device = "cpu"
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
        
    print(f"\nCompute Device Selected: {device.upper()}")
    
    if device == "mps":
        try:
            print("\nAttempting memory stress test (simulating CatVTON SD1.5 attention layer allocations)...")
            start = time.time()
            # CatVTON uses a concatenated UNet which processes Person + Garment + Mask + Condition
            # This requires massive hidden states. We simulate allocating 8GB of float16 tensors.
            tensors = []
            for i in range(8):
                # 1GB tensor
                t = torch.randn(1024, 1024, 256, dtype=torch.float32, device="mps")
                tensors.append(t)
                time.sleep(0.1)
                
            print(f"Memory allocation successful. (Took {time.time() - start:.2f}s)")
            return True
            
        except Exception as e:
            print(f"\n[ERROR] Hardware test failed during tensor allocation: {str(e)}")
            return False
    else:
        print("CUDA/MPS not available. CPU-only Diffusion VTO takes 5-10 minutes per image.")
        return False

if __name__ == '__main__':
    success = check_hardware_for_vton()
    if not success:
        print("\nCONCLUSION: Hardware is INSUFFICIENT for real-time / local Diffusion VTO.")
    else:
        print("\nCONCLUSION: Hardware IS sufficient. Proceeding with pipeline...")
