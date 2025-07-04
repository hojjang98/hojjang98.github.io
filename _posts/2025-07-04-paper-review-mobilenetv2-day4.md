---
layout: post
title: "Paper Review: MobileNetV2 DAY 4"
date: 2025-07-04
categories: paper_review
---

## 📌 Paper Info

- **Title**: *MobileNetV2: Inverted Residuals and Linear Bottlenecks*  
- **Authors**: Mark Sandler, Andrew Howard, Menglong Zhu, Andrey Zhmoginov, Liang-Chieh Chen  
- **Link**: [arXiv 1801.04381](https://arxiv.org/abs/1801.04381)  
- **Published**: 2018 (Google Research)  
- **Code**: Available in TensorFlow-Slim  

---

## 🧠 Day 4 Review – Architecture Implementation in PyTorch

### ✅ Focus

Today’s goal was to turn theory into code — I implemented the MobileNetV2 building block from scratch in PyTorch.

### 🧱 What I Implemented

- **InvertedResidual block**:
  - 1×1 Conv (Expansion) + BatchNorm + ReLU6  
  - 3×3 Depthwise Conv + BatchNorm + ReLU6  
  - 1×1 Conv (Linear projection, no activation)  
  - Optional residual connection if `stride == 1` and `in_channels == out_channels`

```python
class InvertedResidual(nn.Module):
    def __init__(self, in_channels, out_channels, stride, expand_ratio):
        super().__init__()
        hidden_dim = in_channels * expand_ratio
        self.use_res_connect = (stride == 1 and in_channels == out_channels)

        layers = []
        if expand_ratio != 1:
            layers += [
                nn.Conv2d(in_channels, hidden_dim, 1, bias=False),
                nn.BatchNorm2d(hidden_dim),
                nn.ReLU6(inplace=True)
            ]
        layers += [
            nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 1, groups=hidden_dim, bias=False),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU6(inplace=True),
            nn.Conv2d(hidden_dim, out_channels, 1, bias=False),
            nn.BatchNorm2d(out_channels)
        ]
        self.conv = nn.Sequential(*layers)

    def forward(self, x):
        if self.use_res_connect:
            return x + self.conv(x)
        else:
            return self.conv(x)
```

---

### 🔍 Reflections

- The use of **ReLU6** before projection is crucial to avoid destroying information in low-dimensional space  
- Confirmed that **depthwise separable conv + linear bottleneck + skip connections** leads to a very compact and fast block  
- Running shape tests confirmed that residual connections only activate under the right conditions  
- This exercise made the architecture much clearer in terms of **flow, constraints, and design intuition**

---

## ✅ Summary

Implementing the MobileNetV2 block deepened my understanding of how lightweight CNNs are constructed.  
Each design choice — from activation placement to depthwise grouping — serves to optimize for **speed, memory**, and **representational efficiency**.  
This block will serve as a reusable module for future experiments and real-time CV applications.

> 📌 **Note**: Full model accuracy (ACC) evaluation will be updated tomorrow after full inference and validation.