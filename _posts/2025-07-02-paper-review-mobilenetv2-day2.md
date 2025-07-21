---
layout: post
title: "Paper Review: MobileNetV2 DAY 2"
date: 2025-07-02
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

## 🧠 Day 2 Review – Core Architecture Breakdown

### ✅ Step 1: Depthwise Separable Convolution

To reduce computation, MobileNetV2 employs **depthwise separable convolutions**, splitting standard convolution into:
- **Depthwise Convolution**: One filter per input channel (spatial filtering).
- **Pointwise Convolution (1×1)**: Linear combinations across channels.

This reduces computation by a factor of **8–9×** (with `3×3` kernels) while maintaining accuracy, making it ideal for mobile devices.

---

### ✅ Step 2: Linear Bottlenecks

MobileNetV2 removes the ReLU activation from the final 1×1 projection layer in the bottleneck block.  
Why? Because **ReLU can destroy information** in low-dimensional spaces by zeroing out values.  
By keeping this layer linear, the architecture preserves more information while still introducing non-linearity earlier in the block.

---

### ✅ Step 3: Inverted Residuals

Unlike traditional residual blocks (e.g., ResNet) that skip across wide layers, MobileNetV2 **connects compressed bottlenecks**.  
This inverted design:
- Avoids memory-heavy high-dimensional skips  
- Preserves representational power and gradient flow  
- Makes mobile inference more memory-efficient

📌 **Residual connections are only applied if:**
- `stride = 1`, and  
- Input and output dimensions match

---

### ✅ Step 4: Block Structure Summary

Each MobileNetV2 block follows this sequence:

```
Input → 1×1 Conv (Expansion, ReLU6)  
     → 3×3 Depthwise Conv (Stride s, ReLU6)  
     → 1×1 Conv (Projection, Linear)  
     → + Residual connection (if stride = 1 and input/output dims match)
```

- Expansion factor `t = 6` (commonly)
- **ReLU6** is used for stability in low-precision computation
- The final projection is **linear**, forming the "Linear Bottleneck"

This structure is lightweight, modular, and extremely efficient for mobile environments.

---

## ✅ Key Insights (3-Line Summary)

- MobileNetV2 splits convolutions into efficient parts and carefully limits where activation functions are used.  
- Inverted Residuals connect low-dimensional layers for better memory and speed efficiency.  
- Each block combines expansion, filtering, and projection in a way that balances accuracy and performance.

---

## 📘 New Terms

- **Activation manifold**: A low-dimensional structure embedded in high-dimensional activation space  
- **ReLU6**: A ReLU variant capped at 6 to improve quantization stability

---

## 🗂 GitHub Repository

Detailed markdown summary:  
🔗 [github.com/hojjang98/Paper-Review](https://github.com/hojjang98/Paper-Review/blob/main/vision/01_mobilenetv2/summary.md)

---

## 💭 Reflections

The architecture design feels even more elegant now that I’ve broken down its components.  
The use of linear layers and depthwise convolutions shows how theory and engineering blend together.  
Next, I plan to look at experiments, ablation results, and comparisons with MobileNetV1 and ShuffleNet.

---
