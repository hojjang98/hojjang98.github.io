---
layout: post  
title: "Paper Review: Denoising Diffusion Probabilistic Models – DAY 4"  
date: 2025-09-19
categories: paper_review  
---

> 📚 [https://arxiv.org/abs/2006.11239](https://arxiv.org/abs/2006.11239)  
> 🏆 Published in **NeurIPS 2020**

# 📄 Denoising Diffusion Probabilistic Models – Day 4

## ✨ Key Contributions
- Showed that DDPMs achieve **state-of-the-art performance** on CIFAR-10.  
- Demonstrated competitive results on **LSUN** and **CelebA HQ** datasets.  
- Proved diffusion models can match or surpass GANs without adversarial training.  

## 🎯 Problem Definition
- Validate whether diffusion models can produce **high-quality, diverse images** at scale.  
- Compare against GAN-based baselines known for sharp but unstable generation.  

## 🧠 Method / Architecture
- Trained DDPM on **CIFAR-10, LSUN, CelebA HQ**.  
- Evaluated with **Fréchet Inception Distance (FID)** and **Inception Score (IS)**.  
- Focused on stability and diversity compared to GANs.  

## 🧪 Experiments & Results
- **CIFAR-10**: IS = 9.46, FID = 3.17 → state-of-the-art at the time.  
- **LSUN (256×256)**: Image quality on par with ProgressiveGAN.  
- **CelebA HQ**: High-resolution samples with competitive quality.  
- Generated images were **sharp, diverse, and stable**, avoiding mode collapse.  

## 🚫 Limitations
- Computationally expensive compared to GANs (many denoising steps).  
- Sampling speed slower than adversarial approaches.  

## 🔭 Future Ideas
- Explore **faster sampling techniques** to reduce inference cost.  
- Extend experiments to more complex and diverse datasets.  

## 🔁 Personal Reflections
- Impressive to see DDPMs rival GANs without instability.  
- Stability from the **MSE denoising objective** seems like a major breakthrough.  
- This could shift generative modeling away from adversarial setups toward diffusion-based methods.  
