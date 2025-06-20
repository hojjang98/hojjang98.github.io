# 🧠 Daily Study Log [2025-06-19]

Today was all about combining hands-on computer vision tasks with core CNN theory.  
I trained a segmentation model on real urban scenes and revisited a sign language classification task to solidify my understanding of CNN fundamentals.

---

## 🏙️ Image Segmentation — Urban Scene Understanding

- **Objective**: Assign semantic labels (road, sky, building, etc.) to every pixel in an image — essential for self-driving perception.
- **Dataset**: Cityscapes (`_leftImg8bit.png`, `_gtFine_labelIds.png`)
- **Model**: `Unet(resnet34)` from `segmentation_models_pytorch`
- **Input Size**: Resized to 256x256
- **Loss Function**: `CrossEntropyLoss()` with `classes=34`
- **Training**: 5 epochs — loss steadily decreased
- **Result**: Predicted masks matched ground truth very well; roads, skies, cars, and buildings were segmented accurately

✅ **Takeaways**  
- I made a mistake in setting the number of output classes, which helped me understand how `CrossEntropyLoss()` behaves — a valuable learning moment.  
- Semantic segmentation gives *visual* feedback, which made model performance much more intuitive to grasp.

---

## 🧪 CNN Basics Recap — Sign Language Classifier

- **Task**: Classify images of hand gestures into 10 sign language categories
- **Model**: Simple CNN (Conv → ReLU → MaxPool → Dense)
- **Input**: RGB images resized to 224x224
- **Loss**: Categorical CrossEntropy
- **Augmentation**: Horizontal flips, random rotations using `ImageDataGenerator`
- **Performance Check**: Printed classification report and plotted training accuracy

✅ **Reflections**  
- The simple CNN worked decently and was great for reviewing layer flow and preprocessing steps.  
- Reinforced the importance of proper image labeling and class balancing.

---

## 🎯 Next Steps

- Try advanced architectures like **SegFormer** and **DeepLab v3+**
- Evaluate using **mIoU**, **pixel accuracy**, and visualization tools
- Build a proper inference pipeline → Prepare for deployment

---

## ✅ TL;DR

📍 **U-Net: Deployed on urban segmentation**  
📍 **CNN: Refreshed using sign language dataset**  
📍 **Next: Test SegFormer + Evaluate with mIoU**
