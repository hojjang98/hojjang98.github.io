---
layout: post
title: "Paper Review: MobileNetV2 DAY 3"
date: 2025-07-03
categories: paper_review
mathjax: true
---

## 📌 Paper Info

- **Title**: *MobileNetV2: Inverted Residuals and Linear Bottlenecks*  
- **Authors**: Mark Sandler, Andrew Howard, Menglong Zhu, Andrey Zhmoginov, Liang-Chieh Chen  
- **Link**: [arXiv 1801.04381](https://arxiv.org/abs/1801.04381)  
- **Published**: 2018 (Google Research)  
- **Code**: Available in TensorFlow-Slim  

---

## 🧠 Day 3 Review – Experiments, Applications, and Conclusions

### ✅ Step 1: Architecture Expansion

The final MobileNetV2 network consists of:

```bash
Initial 3×3 Conv
→ Repeating Bottleneck Blocks (19 times)
→ Final 1×1 Conv + Global Average Pooling + FC layer
```

- Each block uses an **expansion factor t = 6**  
- All convolutions are 3×3 or 1×1  
- BatchNorm & Dropout applied where appropriate  
- ReLU6 for activation (except final linear projection)

---

### ✅ Step 2: Experimental Results Summary

#### 📍 ImageNet Classification

| Model           | Top-1 Acc | MACs   | Params |
|----------------|-----------|--------|--------|
| MobileNetV1     | 70.6%     | 575M   | 4.2M   |
| **MobileNetV2** | **71.8%** | 300M   | 3.4M   |

→ V2 achieves **better accuracy** with nearly **half the computation**.

#### 📍 Object Detection (COCO, with SSDLite)

| Model                | mAP   | Latency |
|---------------------|-------|---------|
| MobileNetV1 + SSD   | 19.3  | 27 ms   |
| **MobileNetV2 + SSDLite** | **22.1** | **19 ms** |

→ V2 provides **higher mAP** and **faster inference**.

#### 📍 Memory Efficiency

In Table 2 (Fig. 2 in the paper), MobileNetV2 shows **peak memory usage < 400K** during inference.  
This is **lower than ResNet-50, VGG, Inception**, and other baselines.

---

### ✅ Step 3: Applications

- **Object Detection**: Used in real-time detectors like **SSDLite**  
- **Semantic Segmentation**: Combined with DeepLabv3 for mobile segmentation  
- **Mobile Transfer Learning**: Widely used for fine-tuning on edge devices

---

## ✅ Key Insights (3-Line Summary)

- MobileNetV2 achieves strong accuracy with low memory and compute requirements.  
- The architecture outperforms V1 and competes with heavier models in speed and accuracy.  
- It is ideal for on-device inference tasks such as detection and segmentation.

---

## 📘 New Terms

- **MACs (Multiply-Accumulate Ops)**: A proxy for computation cost  
- **mAP (mean Average Precision)**: Detection accuracy averaged across IoU thresholds  
- **Materialized Memory**: Memory required to hold intermediate activations during inference

---

## 🗂 GitHub Repository

Visual summary + experimental table:  
🔗 [github.com/hojjang98/Paper-Review](https://github.com/hojjang98/Paper-Review/blob/main/vision/01_mobilenetv2/summary.md)

---

## 💭 Reflections

The experiments confirm that MobileNetV2 is not just lightweight in theory, but in practice.  
Its memory efficiency and speed make it one of the most impactful mobile architectures of its time.  
I'm especially impressed with how well it balances performance and hardware constraints.

---

