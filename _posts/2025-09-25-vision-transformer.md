---
layout: post  
title: "Paper Review: Vision Transformer – DAY 2"  
date: 2025-09-25
categories: paper_review  
---

> 📚 [https://arxiv.org/abs/2010.11929](https://arxiv.org/abs/2010.11929)  
> 🏆 Published in **ICLR 2021**  

# 📄 Vision Transformer (ViT) – Day 2

## ✨ Key Contributions
- Introduced a **patch-based embedding scheme** to transform images into sequences.  
- Showed how **positional embeddings** are necessary to retain spatial order in vision tasks.  
- Applied the **standard Transformer encoder** directly to visual tokens without convolution.  
- Proposed the use of a **[CLS] token** for classification, similar to BERT.  

---

## 🎯 Problem Definition
- Images do not have a natural sequence like text, so a method was needed to **convert images into token sequences**.  
- Transformers lack inherent order awareness → must find a way to **preserve positional information**.  
- The challenge was to design an architecture that leverages the **global attention** of Transformers while still being effective for vision tasks.  

---

## 🧠 Method / Architecture
1. **Image to Sequence (Patch Embedding)**  
   - Input image is split into fixed-size non-overlapping patches (e.g., 16×16).  
   - Each patch is flattened and linearly projected into a D-dimensional embedding.  
   - The sequence of patch embeddings serves as the Transformer input.  

2. **Positional Encoding**  
   - Since Transformers treat tokens independently, spatial order would be lost.  
   - To preserve location, learnable **positional embeddings** are added to each patch embedding.  

3. **Transformer Encoder**  
   - Standard architecture: Multi-Head Self-Attention + MLP block, with residuals and layer normalization.  
   - Enables **global context modeling** across all image patches.  

4. **Classification Head**  
   - A special **[CLS] token** is prepended to the patch sequence.  
   - After passing through the encoder, the final hidden state of [CLS] is used by an MLP head for classification.  

---

## 🧪 Experiments & Results
- Early experiments confirm that this pipeline allows Transformers to process images **without convolutions**.  
- Showed the feasibility of patch embedding + positional encoding as a robust replacement for convolutional inductive biases.  

---

## 🚫 Limitations
- Still computationally heavy due to quadratic self-attention on large patch sequences.  
- Requires careful patch sizing: too small → computational explosion, too large → loss of detail.  

---

## 🔭 Future Ideas
- Explore **hierarchical patching** (multi-scale representations).  
- Investigate **sparse or efficient attention** mechanisms to reduce cost.  
- Apply patch embeddings to other CV tasks beyond classification.  

---

## 🔁 Personal Reflections
- The **patch embedding idea** feels simple yet revolutionary—it bridges the gap between images and text processing.  
- Interesting how **positional embeddings** become crucial in vision, just like in NLP.  
- The [CLS] token reuse shows the elegance of adapting existing NLP concepts into CV.  
