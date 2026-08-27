# 🚀 IDM-VTON (Hugging Face) Integration Guide

This document explains how to activate the state-of-the-art **IDM-VTON** model using the pre-built `HuggingFaceVTONEngine` in your Aura backend. 

By using the free Hugging Face API, you bypass all local hardware limitations (like the GTX 1050's 4GB VRAM constraint, or Mac's lack of CUDA). Your Mac or Windows machine will route the heavy processing to massive A100 Cloud GPUs for photorealistic results in seconds.

---

## 1. How it works (The Code is Already Written!)

You don't need to write any new code to implement this! The integration is completely finished and located in:
`apps/fitting/engines/huggingface_vton.py`

This engine uses the `gradio_client` library to securely connect to Hugging Face and pass your images to their cloud computers.

## 2. Setting it up in your Admin Panel

You can activate this engine for your live website directly through your Django Admin interface without changing any code:

1. **Start your server** and go to `http://localhost:8000/admin`
2. **Navigate to:** Core > Global Settings
3. **Change the VTO Engine:**
   - Find the dropdown labeled **VTO Engine**
   - Change it from `Local API` to `Cloud API: Hugging Face Spaces`
4. **Configure Hugging Face Settings:**
   - **HF Space ID:** Type exactly `yisol/IDM-VTON`
   - **HF API Token:** Paste your free token here (see step 3 below).

## 3. How to get your free Hugging Face Token

To prevent the `You have exceeded your ZeroGPU quota` rate limit we saw earlier, you just need to pass a free account token.

1. Go to [https://huggingface.co/join](https://huggingface.co/join) and create a free account.
2. Log in and go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
3. Click **"Create new token"** (A "Read" token is perfectly fine).
4. Copy the token (it starts with `hf_...`) and paste it into your Django Admin Global Settings.

## 4. Mac Deployment Notes

If you or your team switch to developing on a Mac, you won't be able to run local Nvidia CUDA models anyway. 

By setting your `VTO Engine` to `Hugging Face Spaces` in your database, your Mac will flawlessly generate images by routing them to the cloud. Just ensure your Mac's virtual environment has the required library installed:

```bash
pip install gradio_client
```

---
*Ready for Git:* You can commit this file to your repository so your team knows how to configure the high-quality VTO model without crashing their local machines!
