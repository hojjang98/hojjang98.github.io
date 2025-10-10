---
layout: post  
title: "Paper Review: InternVideo2 – DAY 3"  
date: 2025-10-10  
categories: paper_review  
---

> 📚 [https://arxiv.org/abs/2403.15377](https://arxiv.org/abs/2403.15377)  
> 🏆 Published in **CVPR 2024 (Best Paper Honorable Mention)**  

# 📄 InternVideo2 – Scaling Video Foundation Models for Multimodal Understanding  

## ✨ Key Contributions  
- Demonstrates **scalable pretraining** across **400M multimodal video–text pairs (InternVid-400M)**.  
- Combines three key objectives — **Masked Video Modeling (MVM)**, **Contrastive Learning (CL)**, and **Next-Token Generation (GEN)** — in a **progressive curriculum**.  
- Utilizes **massive multimodal datasets** (video, text, audio, speech) to enhance generalization and zero-shot transfer.  
- Establishes a highly **efficient pretraining pipeline** using **DeepSpeed**, **FlashAttention**, and **BF16 precision** across 1024 GPUs.  

---

## 🎯 Problem Definition  
- Training multimodal video models at scale poses challenges in **data diversity, efficiency, and optimization stability**.  
- Previous large-scale vision–language models often lacked **audio or temporal integration**, limiting multimodal understanding.  
- InternVideo2 addresses these issues through a **unified pretraining framework** optimized for scalability, diversity, and multimodal synergy.  

---

## 🧠 Method / Architecture  

### 1️⃣ Multimodal Datasets  
InternVideo2 pretrains on one of the largest multimodal corpora ever assembled:  

| Dataset | Type | Size | Key Feature |
|----------|------|------|--------------|
| **InternVid-400M** | Video–Text | 400M | Core dataset with diverse, high-quality captions |
| **WebVid2.5M** | Video–Text | 2.5M | Natural human actions and scenes |
| **CC3M / CC12M** | Image–Text | 15M | Provides additional textual grounding |
| **AudioSet** | Video–Audio | 2M | Adds robust audio modality learning |
| **HowTo100M** | Instructional Video | 100M | Rich temporal and linguistic alignment |

➡️ **Data diversity** is crucial to achieving strong multimodal generalization and cross-domain robustness.  

---

### 2️⃣ Pretraining Pipeline  
InternVideo2 follows a **three-stage progressive training framework**:

| Stage | Objective | Description |
|--------|------------|-------------|
| **Stage 1 – Masked Video Modeling (MVM)** | Reconstruction | Learns low-level spatial–temporal representations by recovering masked video patches. |
| **Stage 2 – Multimodal Contrastive Learning (CL)** | Alignment | Aligns representations across video, text, audio, and speech using CLIP-style contrastive loss. |
| **Stage 3 – Next-Token Prediction (GEN)** | Generation | Trains causal decoding for generative tasks such as captioning and dialogue reasoning. |

Each stage builds upon the previous one, gradually improving both **representation quality** and **cross-modal coherence**.  

---

### 3️⃣ Training Configuration  

| Setting | Value |
|----------|--------|
| **Model Size** | 1B → 6B parameters |
| **Optimizer** | AdamW |
| **Learning Rate** | 1e-4 (cosine decay) |
| **Batch Size** | 16K video clips |
| **Hardware** | 1024 × NVIDIA A100 (80GB) |
| **Precision** | FP16 / BF16 |
| **Framework** | DeepSpeed + FlashAttention |
| **Training Duration** | ≈ 2 months (for 6B model) |

> 💡 Efficiency boosted via **gradient checkpointing**, **distributed memory bank**, and **mixed precision training**.

---

### 4️⃣ Fine-Tuning Strategy  

| Task | Dataset | Objective |
|------|----------|------------|
| **Video–Text Retrieval** | MSR-VTT, VATEX | Contrastive |
| **Action Recognition** | Kinetics-400, SSv2 | Cross-Entropy |
| **Video Captioning** | MSVD, MSR-VTT | Causal LM |
| **Audio–Visual QA** | NExT-QA, AVQA | Multimodal reasoning |

**Tip:** During fine-tuning, early spatial layers are frozen, while **temporal and fusion modules** are adapted using LoRA for parameter efficiency.  

---

## 🧪 Experiments & Results  
- The combined **MVM + CL + GEN** objectives significantly improve **zero-shot generalization**.  
- Pretrained InternVideo2 achieves state-of-the-art results on **retrieval**, **captioning**, and **action recognition** benchmarks.  
- Data scaling from millions to hundreds of millions of pairs follows a clear **scaling law**, where larger data → better generalization.  

---

## 🚫 Limitations  
- Requires extremely **high computational cost** and massive distributed training infrastructure.  
- Sensitive to **imbalanced modality distributions** (e.g., when one modality is underrepresented).  
- Current training still relies heavily on **curated video–text data** rather than real-world noisy sources.  

---

## 🔭 Future Ideas  
- Incorporate **unsupervised multimodal data** to enhance robustness.  
- Explore **adaptive data sampling** strategies to balance modality contributions.  
- Apply **efficient fine-tuning** techniques (adapters, LoRA, QLoRA) for smaller-scale domains.  

---

## 🔁 Personal Reflections  
- The scale of InternVideo2’s dataset and pretraining pipeline clearly demonstrates the **power of multimodal scaling laws**.  
- The **progressive curriculum** (MVM → CL → GEN) ensures stable optimization and richer feature learning.  
- This stage marks the true evolution from simple video-language models to **foundation-level multimodal learners**.  
- Overall, InternVideo2 sets a new benchmark for **scalable, unified multimodal understanding** across vision, language, and audio.  
