---
layout: post  
title: "Paper Review: Few-Shot Adaptation of Grounding DINO for Agricultural Domain – DAY 3"  
date: 2025-08-18  
categories: paper_review  
mathjax: true  
---

> 📚 [https://arxiv.org/abs/2504.07252](https://arxiv.org/abs/2504.07252)  

## ✅ Day 3 – Experiments & Results

Today I reviewed the **Experiments & Results** section of the paper, focusing on how the proposed few-shot adaptation compares to zero-shot and fully fine-tuned baselines across agricultural and cross-domain datasets.

---

### 📌 Experimental Setup

- **Datasets**:  
  - Agricultural benchmarks: crop/weed detection, fruit counting, insect identification, wheat head detection, and PhenoBench.  
  - Cross-domain: remote sensing datasets for additional validation.  

- **Baselines**:  
  - Zero-shot Grounding DINO (prompt-based)  
  - Fully fine-tuned YOLO models  
  - Other state-of-the-art methods  

---

### 📌 Main Results

- On agricultural datasets, the proposed **few-shot adaptation** outperformed fully fine-tuned YOLO by **up to +24% mAP**.  
- In remote sensing, it improved over SOTA baselines by about **+10%**.  
- Zero-shot performed reasonably in simple settings but failed in **complex, cluttered environments** (e.g., occluded crops, mixed weeds). Few-shot adaptation alleviated these issues.  

---

### 📌 Effect of Shot Number

- **1-shot**: Performance can drop below zero-shot in multi-class scenarios due to limited class coverage.  
- **4-shot & 16-shot**: Steady improvement in mAP as the number of labeled samples increases.  
- **Instance segmentation (PhenoBench + SAM2)**:  
  - 1-shot produced reasonable mask mAP.  
  - 8-shot significantly boosted segmentation performance.  

---

### 📌 Summary Table

| Aspect | Zero-shot (Prompt-based) | Few-shot (Proposed) |
|--------|---------------------------|----------------------|
| Data Requirement | Only text prompts | ≥2 labeled images per class |
| Prompt Design | Manual, error-prone | Not required |
| Trainable Params | Fixed prompts | Only embeddings |
| Performance | Good in simple cases, weak in complex ones | Up to +24% mAP over YOLO, +10% over SOTA |
| Cross-domain | Limited | Validated on remote sensing |

---

### 🧠 Final Thoughts

The experiments confirm that **few-shot embedding adaptation** delivers substantial improvements with minimal labeled data.  
It eliminates the need for prompt engineering, remains parameter-efficient, and generalizes well across domains — making it a **practical solution for data-scarce environments**.
