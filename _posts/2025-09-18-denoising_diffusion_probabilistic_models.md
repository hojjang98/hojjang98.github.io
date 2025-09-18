---
layout: post  
title: "Paper Review: Denoising Diffusion Probabilistic Models – DAY 3"  
date: 2025-09-18
categories: paper_review  
---

> 📚 [https://arxiv.org/abs/2006.11239](https://arxiv.org/abs/2006.11239)  
> 🏆 Published in **NeurIPS 2020**

## ✅ Day 3 – Reverse Process (Denoising)  

---

### 📌 What is the Reverse Process?  
- While the forward process gradually destroys data by adding noise, the **reverse process** tries to undo this corruption step by step.  
- The challenge is that the true reverse distribution is **intractable**, so we need to approximate it.  

---

### 📌 Gaussian Approximation  
- The reverse step is assumed to be **Gaussian as well**, which makes the math manageable.  
- Instead of knowing the exact distribution, we let a **neural network** learn the parameters (mean and variance) that guide how to denoise the data.  

---

### 📌 Noise Prediction Network  
- A key trick: instead of predicting the clean data directly, the network is trained to predict the **noise that was added**.  
- The model takes the noisy input and the timestep as input, and outputs an estimate of the noise.  
- Once the noise is known, the clean signal can be reconstructed.  

---

### 📌 Training Objective  
- The training boils down to a **simple mean squared error (MSE)** between the true noise and the predicted noise.  
- In other words, the model learns to **remove noise step by step**, making the data clearer at each stage.  

---

### 📌 Key Notes  
- The reverse process is the **only part that is learned** in diffusion models.  
- The training is relatively stable because it reduces to a standard denoising task.  
- This denoising idea is the **core mechanism** that powers DDPMs.  

---

### 🧠 Final Thoughts (Day 3)  
Day 3 showed me that the reverse process is all about **learning how to clean up noise**.  
By reframing the problem into predicting noise with a simple loss function, diffusion models become both **trainable and effective**.  
This step is where the true **generative power** of the model emerges.  
