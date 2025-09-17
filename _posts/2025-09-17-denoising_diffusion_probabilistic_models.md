---
layout: post  
title: "Paper Review: Denoising Diffusion Probabilistic Models – DAY 2"  
date: 2025-09-17
categories: paper_review  
mathjax: true  
---

> 📚 [https://arxiv.org/abs/2006.11239](https://arxiv.org/abs/2006.11239)  
> 🏆 Published in **NeurIPS 2020**

## ✅ Day 2 – Forward Process (Noising)  

---

### 📌 What is the Forward Process?  
- The forward process is the **destruction phase**: it takes real data and gradually turns it into pure noise.  
- This is done step by step in a **Markov chain**, where each step only depends on the previous one.  
- At the end of the process, no matter what the original data was, it becomes indistinguishable Gaussian noise.  

---

### 📌 How It Works  
- At each step, a small amount of Gaussian noise is added.  
- The noise amount is controlled by a **variance schedule** (β values), which decides how quickly the data is corrupted.  
- Because the noise is added gradually, the process is **smooth and stable**.  

---

### 📌 Key Properties  
1. **No learning required** – the forward process is completely predefined and fixed.  
2. **Direct sampling possible** – we can jump directly to any noisy version of the data without simulating every step.  
3. **Guaranteed convergence** – after enough steps, all data points look like random Gaussian noise.  

---

### 📌 Intuition  
- Imagine starting with a clean photo and adding a tiny blur or static every time.  
- After many steps, the photo becomes so noisy that the original content is completely gone.  
- This gives the reverse process (the model we train) a **clear and structured task**: recover the data step by step in the opposite direction.  

---

### 🧠 Final Thoughts (Day 2)  
Day 2 showed me that diffusion models are built on a very **simple but powerful idea**:  
systematically destroy data in a way that is mathematically controlled, so that we can later learn how to reverse it.  
This forward process acts as the **blueprint** for how the generative model will be trained.  
