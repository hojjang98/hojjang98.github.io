---
layout: post  
title: "Paper Review: Denoising Diffusion Probabilistic Models – DAY 1"  
date: 2025-09-16
categories: paper_review  
mathjax: true  
---

> 📚 [https://arxiv.org/abs/2006.11239](https://arxiv.org/abs/2006.11239)  
> 🏆 Published in **NeurIPS 2020**

## ✅ Day 1 – Abstract & Introduction  

---

### 📌 Background & Motivation  
- Deep generative models (GANs, VAEs, autoregressive, flow-based) achieved strong results but had **critical weaknesses**:  
  - **VAE**: blurry samples from variational approximations  
  - **GAN**: unstable training, mode collapse  
  - **Flow-based**: heavy inductive biases, complex designs  
- These issues motivated a **new direction** for stable, high-quality generation.  

---

### 📌 Core Idea  
- Reframe generation as a **denoising process**.  
- **Forward process**: add Gaussian noise step by step until data becomes pure noise.  
- **Reverse process**: learn to remove noise progressively, reconstructing data from random noise.  
- Gaussian formulation enables **simple neural network training**.  

---

### 📌 Main Contributions  
1. Produces **high-quality synthesis**, rivaling or beating GANs.  
2. **Stable training** without adversarial tricks.  
3. **Simple MSE objective** → predict noise directly.  
4. Shows a **theoretical link** between diffusion models, denoising score matching, and Langevin dynamics.  

---

### 📌 Early Results  
- **CIFAR-10**: IS = 9.46, FID = 3.17 (state-of-the-art at the time).  
- **LSUN 256×256**: rivaled **ProgressiveGAN** in sample quality.  

---

### 📌 Key Takeaways (Day 1)  
1. Diffusion models redefine generation as **noise removal**.  
2. Avoid major drawbacks of GANs/VAEs with stable training.  
3. Achieve **SOTA results** with a simple and interpretable framework.  

---

### 🧠 Final Thoughts (Day 1)  
Day 1 shows how diffusion models emerged as a **clean, stable alternative** to adversarial or variational approaches.  
The elegance of turning generation into **progressive denoising** laid the foundation for their rapid adoption in vision tasks.  
