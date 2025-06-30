---
layout: post
title: "Daily Study Log 31"
date: 2025-05-21
category: study_log
---

# 🏙️ [2025-06-19] Urban Scene Segmentation & CNN Recap

Today was a productive day filled with hands-on practice in image segmentation and a solid CNN refresher.  
I trained a U-Net model to predict pixel-wise masks on real urban scenes and verified that the predictions matched the ground truth closely.  
In parallel, I revisited the classic Dog vs. Cat classifier to reinforce CNN basics.

---

## 🧱 1. Image Segmentation — Urban Street Scenes

This project tackles **semantic segmentation** on urban environments using the **Cityscapes dataset**.  
The goal was to assign each pixel a semantic label (e.g., road, sky, building) — a key component for autonomous driving systems.

### ✅ Technical Highlights
- **Dataset**: Cityscapes (`_leftImg8bit.png`, `_gtFine_labelIds.png`)
- **Model**: `Unet(resnet34)` from `segmentation_models_pytorch`
- **Loss Function**: `CrossEntropyLoss()` with `classes=34`
- **Input Size**: Resized to 256x256
- **Training**: 5 epochs with steadily decreasing loss
- **Evaluation**: Visual comparison between predicted and ground truth masks showed strong alignment

### 🖼️ Sample Visualization
- Displayed side-by-side plots of Input Image, Ground Truth Mask, and Predicted Mask  
- Road, buildings, sky, and vehicles were segmented accurately

---

## 🧪 2. CNN Recap — Dog vs. Cat Classifier

As a complementary activity, I reviewed a basic CNN model using the Dog vs. Cat dataset.  
This helped reinforce my understanding of convolutional layers, activation functions, and data preprocessing.

### ✅ Key Elements
- **Input**: RGB images (224x224)
- **Model**: Basic CNN — Conv → ReLU → MaxPool → Dense
- **Loss**: Binary CrossEntropy
- **Augmentation**: Horizontal flip, rotation using `ImageDataGenerator`
- **Performance Check**: Visualized accuracy and loss curves

---

## 💡 Reflections

- **Segmentation offers much more visual intuition than plain classification.**
- I made a mistake in setting the number of output classes, which helped me fully understand how `CrossEntropyLoss()` works — lesson learned.
- It was satisfying to see how well the predicted mask aligned with the ground truth.
- CNN fundamentals are solid now, and I can clearly see the value of transfer learning for more efficient workflows.

---

## 🎯 Final Thoughts

This session combined practical low-level vision tasks with high-level architectural understanding.  
Next, I plan to experiment with **SegFormer**, **DeepLab v3+**, and evaluate models using **mIoU**, **pixel accuracy**, and **visual comparisons**.

---

✅ **Segmentation: Deployed and working**  
🐶 **CNN: Refreshed and reinforced**  
📈 **Next Step: Validation loop, mIoU scoring, model deployment**
