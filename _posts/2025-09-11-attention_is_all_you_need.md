---
layout: post  
title: "Paper Review: Attention Is All You Need – DAY 3 & 4"  
date: 2025-09-11
categories: paper_review  
mathjax: true  
---

> 📚 [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)  
> 🏆 Published in **NeurIPS 2017**

## ✅ Day 3 – Multi-Head Attention  

---

### 📌 Motivation  
- A single attention head may capture only one type of relationship.  
- Multi-Head Attention lets the model look at different subspaces and positions simultaneously.  

---

### 📌 Mechanism  
- Instead of one attention function, the model projects Queries, Keys, and Values multiple times with different learned weights.  
- Each head runs Scaled Dot-Product Attention independently.  
- The outputs of all heads are concatenated and then linearly transformed again.  

---

### 📌 Dimensions  
- In the paper: number of heads = 8.  
- Each head works on smaller dimensions (64 per head), which keeps computation cost similar to a single large attention.  

---

### 📌 Benefits  
- **Diversity**: each head can focus on different cues (syntax, semantics, positional).  
- **Efficiency**: splitting into smaller heads reduces the computation burden.  
- **Expressiveness**: combining multiple heads enriches the final representation.  

---

### 📌 Key Takeaways (Day 3)  
- Multi-Head Attention = many attentions in parallel.  
- Captures multiple dependencies at once.  
- Core component for the Transformer’s success.  

---

## ✅ Day 4 – Feed-Forward Networks & Positional Encoding  

---

### 📌 Feed-Forward Networks  
- Each encoder/decoder layer has a fully connected feed-forward network after attention.  
- Applied independently at every position, but parameters are shared across all positions.  
- In the paper: input/output size = 512, inner hidden size = 2048.  
- Purpose: adds non-linear transformations, giving the model more capacity.  

---

### 📌 Positional Encoding  
- Transformers don’t have recurrence or convolution → they need a way to know token order.  
- Solution: add positional encodings to embeddings.  
- Defined with sine and cosine functions of different frequencies.  
- Provides both absolute position information and relative distance cues.  

---

### 📌 Why Sinusoidal?  
- Generalizes to sequences longer than those seen during training.  
- Smoothly represents positions and distances.  
- Simple, parameter-free design that works effectively.  

---

### 📌 Key Takeaways (Day 4)  
- FFN: boosts model power with extra transformation at each position.  
- Positional encoding: injects order into an attention-only model.  
- Sinusoidal design: elegant and effective for long sequences.  

---

### 🧠 Final Thoughts (Day 3 & 4)  
- Multi-Head Attention enriches relationships and is the backbone of the Transformer.  
- Feed-Forward Networks add essential non-linearity.  
- Positional Encoding elegantly solves the order problem.  

Next, I’ll study the **training strategies and optimization details** described in the paper.  
