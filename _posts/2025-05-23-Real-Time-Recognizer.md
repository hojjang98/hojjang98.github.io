## 🧪 Tuning the Recognizer – Dropout, Dense, and Fine-Tuning

After my first MobileNetV2-based classifier, I wasn’t quite satisfied.  
**0.55 validation accuracy** was solid for a start, but I knew the model could do better.

So I rolled up my sleeves and tried again — this time with a more aggressive strategy.

---

### 🔁 What I Changed

- 🔧 **Fine-tuned** the **last 40 layers** of MobileNetV2 instead of freezing the whole base
- 💡 Expanded the classifier: `GlobalAveragePooling → Dense(256) → Dropout(0.3) → Dense(128) → Softmax`
- ⚙️ Kept using the `Adam` optimizer and all previous callbacks

---

### 📊 Results

| Metric | Value |
|--------|--------|
| **Train Accuracy** | 0.7065 |
| **Validation Accuracy** | 0.5891 |
| **Train Loss** | 0.8010 |
| **Validation Loss** | 1.0707 |

While not a breakthrough, it was a **clear improvement** — both in training and validation performance.  
Validation accuracy rose nearly **+3%**, and train loss dropped significantly.

---

### 💡 What I Learned Today

- 🔄 **Fine-tuning MobileNetV2** yields better representations when more layers are unfrozen
- 🔍 Deeper Dense layers helped the classifier become more expressive
- 📉 The model began to generalize slightly better, though it’s still not perfect

---

### 🎯 Next Target: 70%

- Current validation accuracy: **~59%**
- Short-term goal: **surpass 60%**
- Long-term mission: **break the 70% wall**

Tomorrow, I plan to **expand the dataset** — aiming for **~1000 images per class**.  
Let’s see how far that can push us.
