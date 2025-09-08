---
layout: post  
title: "Paper Review: Attention Is All You Need – DAY 2"  
date: 2025-09-08
categories: paper_review  
mathjax: true  
---

> 📚 [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)  
> 🏆 Published in **NeurIPS 2017**

## ✅ Day 2 – Encoder–Decoder & Scaled Dot-Product Attention  

Today I continued with the Transformer paper, focusing on the **model architecture** and the core mechanism of **Scaled Dot-Product Attention**.  

---

### 📌 Encoder–Decoder Architecture  

- Like many sequence transduction models, the Transformer keeps an **encoder–decoder structure**.  
- The **encoder** reads the input sequence and produces a series of continuous representations.  
- The **decoder** generates the output sequence step by step, autoregressively using previously generated tokens as context.  

---

### 📌 Transformer Encoder  

- Built from **6 identical layers**, each containing:  
  1. A **multi-head self-attention** mechanism  
  2. A **feed-forward network** applied to each position independently  
- To stabilize training, every sub-layer applies a **residual connection** followed by **layer normalization**.  
- All layers and embeddings share the same dimensionality, making the architecture consistent.  

---

### 📌 Transformer Decoder  

- Also made of **6 identical layers**, but with one extra sub-layer compared to the encoder:  
  1. **Masked self-attention** to prevent attending to future tokens  
  2. **Encoder–decoder attention** to incorporate encoder outputs  
  3. **Feed-forward network**  
- The masking is key: it ensures that predictions at position *i* depend only on the outputs before *i*.  

---

### 📌 What Is Attention?  

- Attention can be thought of as a way to **look up information**.  
- A **query** asks a question, **keys** act as the index, and **values** contain the actual content.  
- The model compares the query with all keys, assigns weights, and produces a weighted sum of the values.  

---

### 📌 Scaled Dot-Product Attention  

- The Transformer uses a special form of attention called **Scaled Dot-Product Attention**.  
- Steps:  
  1. Compute similarity between queries and keys using dot products.  
  2. Scale the results by the size of the key dimension (to keep values stable).  
  3. Apply a **softmax** to turn similarities into probabilities.  
  4. Use these probabilities as weights to combine the values.  
- The result is a representation where each token can selectively focus on other relevant tokens.  

---

### 📌 Additive vs Dot-Product Attention  

- **Additive attention** uses a small neural network to compare queries and keys.  
- **Dot-product attention** is simpler and faster since it relies on matrix multiplication, which is highly optimized on GPUs.  
- Without scaling, dot-product attention can become unstable for high-dimensional vectors. Scaling fixes this.  

---

### 🧠 Final Thoughts (Day 2)  

This section showed me **how the Transformer is built from attention blocks**:  
- The encoder and decoder are stacks of simple yet powerful layers.  
- Residuals and normalization make deep training feasible.  
- Scaled Dot-Product Attention is the **core building block**, efficient and stable even for large models.  

Next, I’ll explore **Multi-Head Attention**, which extends this mechanism to capture different types of relationships simultaneously.  
