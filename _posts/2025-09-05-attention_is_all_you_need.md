---
layout: post  
title: "Paper Review: Attention Is All You Need – DAY 1"  
date: 2025-09-05  
categories: paper_review  
mathjax: true  
---

> 📚 [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)  
> 🏆 Published in **NeurIPS 2017**

## ✅ Day 1 – Abstract & Introduction  

Today I started reviewing the **Transformer** paper, *“Attention Is All You Need”*. This first step focused on understanding the **motivation, high-level idea, and contributions** of the architecture.

---

### 📌 Background & Motivation  

- Previous **sequence transduction models** mainly used **RNNs/LSTMs/GRUs** or **CNNs** in encoder–decoder frameworks.  
- These recurrent/convolutional models often integrated **attention** to improve performance.  
- However, they faced fundamental issues:  
  - **Sequential computation** → prevented parallelization  
  - **Difficulty with long sequences** (slow training, memory bottlenecks)  
  - **High computational cost**, limiting scalability  

---

### 📌 Proposed Approach  

- The paper introduces the **Transformer**, a new model that:  
  - **Eliminates recurrence and convolution entirely**  
  - Relies **solely on attention mechanisms** for sequence modeling  
- Benefits include:  
  - **Full parallelization** across sequence elements  
  - **Faster training** compared to RNNs/CNNs  
  - Better capture of **long-range dependencies**  

---

### 📌 Key Contributions  

1. First **attention-only architecture**, removing recurrence/convolution.  
2. Enables **parallel computation**, boosting GPU efficiency.  
3. Achieves **state-of-the-art translation performance**:  
   - WMT 2014 English→German: **28.4 BLEU** (+2 over prior SOTA)  
   - WMT 2014 English→French: **41.8 BLEU** (new single-model record)  
4. Shows **generalization** beyond translation (e.g., English constituency parsing).  

---

### 📌 High-Level Workflow  

1. **Traditional models**: update hidden states sequentially → bottleneck.  
2. **Problem**: recurrence blocks parallelization, slows down training.  
3. **Transformer**: directly attends over all tokens at once via attention.  
4. **Outcome**: faster training, better generalization, and improved performance.  

---

### 📌 Early Results  

- Achieved SOTA results with only **12 hours of training on 8 P100 GPUs**.  
- Training cost significantly lower than recurrent/convolutional models.  
- Demonstrated that **attention-only design** is both **efficient and powerful**.  

---

### 🧠 Final Thoughts (Day 1)  

This introduction made clear why the **Transformer** became a paradigm shift:  
- It solved the **parallelization bottleneck** of RNNs.  
- It scaled well with hardware and data.  
- Even in its first version, it outperformed established models at lower cost.  

The next step will be to dive deeper into the **model architecture** — encoder, decoder, and the details of **self-attention**.  
