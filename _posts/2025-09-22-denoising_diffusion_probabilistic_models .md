---
layout: post  
title: "Paper Review: Denoising Diffusion Probabilistic Models – DAY 5"  
date: 2025-09-22
categories: paper_review  
---

> 📚 [https://arxiv.org/abs/2006.11239](https://arxiv.org/abs/2006.11239)  
> 🏆 Published in **NeurIPS 2020**

# 📄 Denoising Diffusion Probabilistic Models – Day 5

## ✨ Key Contributions
- Positioned diffusion models as a **strong alternative** to GANs and VAEs.  
- Highlighted training stability with a simple objective.  
- Connected diffusion to **score matching** and **Langevin dynamics**, providing theoretical grounding.  

## 🎯 Problem Definition
- Assess whether diffusion can serve as a **general-purpose generative framework** beyond images.  
- Identify core challenges like efficiency and computational cost.  

## 🧠 Method / Architecture
- Summarized prior experimental results and theoretical analysis.  
- Framed diffusion as **“add noise → learn to remove noise”**, emphasizing simplicity and power.  

## 🧪 Experiments & Results
- Built upon Day 4 results: competitive or superior to GANs in image generation.  
- Showed **stable and diverse samples** without mode collapse.  
- Validated the framework’s robustness across datasets.  

## 🚫 Limitations
- **Slow sampling** (hundreds to thousands of denoising steps).  
- **High compute requirements** compared to GANs.  

## 🔭 Future Ideas
- Develop **faster samplers** (e.g., DDIM, latent diffusion).  
- Extend to new domains (audio, video, text, multimodal).  
- Explore **hybrid models** combining diffusion with other generative paradigms.  

## 🔁 Personal Reflections
- The final discussion confirms diffusion models are not just a niche, but a **foundational paradigm** in modern generative AI.  
- Despite efficiency limits, their stability and versatility make them central to recent breakthroughs like **Stable Diffusion, Imagen, and DALL·E 2**.  
