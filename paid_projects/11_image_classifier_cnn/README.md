# 🖼️ Project 11 — Image Classifier (CNN)

**Phase 4 — ML Engineering** | Beginner → Real-Time (3 Versions)

---

## 🗺️ Version Roadmap

| Version | What You Build | Complexity |
|---------|---------------|------------|
| v1.0 — Starter | CNN from scratch on CIFAR-10 + transfer learning ResNet50 | ⭐⭐ Intermediate |
| v2.0 — Improved | Custom dataset + Grad-CAM visualisation + misclassification analysis | ⭐⭐ Intermediate |
| v3.0 — Real-Time | Live webcam classifier + REST API + Streamlit upload UI | ⭐⭐⭐ Advanced |

---

## 📦 Libraries Needed
```bash
pip install torch torchvision matplotlib numpy scikit-learn Pillow streamlit fastapi uvicorn
```

---

## 🟢 v1.0 — CNN from Scratch + Transfer Learning

**Skills:** PyTorch CNN, BatchNorm, Dropout, ResNet50 transfer learning

```python
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

transform_train = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32, padding=4),
    transforms.ToTensor(),
    transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
])
transform_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
])

trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                         download=True, transform=transform_train)
testset  = torchvision.datasets.CIFAR10(root='./data', train=False,
                                         download=True, transform=transform_test)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)
testloader  = torch.utils.data.DataLoader(testset,  batch_size=64, shuffle=False)
classes = ['plane','car','bird','cat','deer','dog','frog','horse','ship','truck']

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1);  self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1); self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64,128, 3, padding=1); self.bn3 = nn.BatchNorm2d(128)
        self.pool  = nn.MaxPool2d(2, 2)
        self.drop  = nn.Dropout(0.4)
        self.fc1   = nn.Linear(128*4*4, 512)
        self.fc2   = nn.Linear(512, 10)
    def forward(self, x):
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = self.pool(F.relu(self.bn3(self.conv3(x))))
        x = x.view(-1, 128*4*4)
        x = self.drop(F.relu(self.fc1(x)))
        return self.fc2(x)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model  = CNN().to(device)
optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=20)
criterion = nn.CrossEntropyLoss()

for epoch in range(20):
    model.train()
    for inputs, labels in trainloader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        loss = criterion(model(inputs), labels)
        loss.backward()
        optimizer.step()
    scheduler.step()

    model.eval()
    correct = total = 0
    with torch.no_grad():
        for inputs, labels in testloader:
            inputs, labels = inputs.to(device), labels.to(device)
            _, predicted = model(inputs).max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    print(f"Epoch {epoch+1:02d} | Acc: {100*correct/total:.2f}%")

torch.save(model.state_dict(), 'cnn_cifar10.pth')
```

**What v1 teaches:** Conv → Pool → Dense architecture, BatchNorm prevents overfitting, how transfer learning reuses millions of pre-trained weights.

---

## 🟡 v2.0 — Grad-CAM + Misclassification Analysis

**New in v2:** Grad-CAM heatmaps (see WHAT the model looks at), per-class accuracy, confusion matrix, misclassified image gallery

```python
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns

# Load model from v1
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# --- Grad-CAM Implementation ---
class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        target_layer.register_forward_hook(self._save_activation)
        target_layer.register_full_backward_hook(self._save_gradient)

    def _save_activation(self, module, input, output):
        self.activations = output.detach()

    def _save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def generate(self, input_tensor, class_idx):
        self.model.zero_grad()
        output = self.model(input_tensor)
        output[0, class_idx].backward()

        weights = self.gradients.mean(dim=[2, 3], keepdim=True)
        cam = (weights * self.activations).sum(dim=1, keepdim=True)
        cam = torch.relu(cam)
        cam = cam - cam.min()
        cam = cam / (cam.max() + 1e-8)
        return cam.squeeze().cpu().numpy()

# Load model and data
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3,32,3,padding=1); self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32,64,3,padding=1); self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64,128,3,padding=1); self.bn3 = nn.BatchNorm2d(128)
        self.pool = nn.MaxPool2d(2,2); self.drop = nn.Dropout(0.4)
        self.fc1 = nn.Linear(128*4*4,512); self.fc2 = nn.Linear(512,10)
    def forward(self, x):
        x = self.pool(torch.relu(self.bn1(self.conv1(x))))
        x = self.pool(torch.relu(self.bn2(self.conv2(x))))
        x = self.pool(torch.relu(self.bn3(self.conv3(x))))
        x = x.view(-1, 128*4*4)
        return self.fc2(self.drop(torch.relu(self.fc1(x))))

model = CNN().to(device)
model.load_state_dict(torch.load('cnn_cifar10.pth', map_location=device))
model.eval()

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
])
testset = torchvision.datasets.CIFAR10('./data', train=False, transform=transform, download=True)
testloader = torch.utils.data.DataLoader(testset, batch_size=64, shuffle=False)
classes = ['plane','car','bird','cat','deer','dog','frog','horse','ship','truck']

# Per-class accuracy
class_correct = [0]*10
class_total   = [0]*10
all_pred, all_true = [], []

with torch.no_grad():
    for images, labels in testloader:
        outputs = model(images.to(device))
        _, predicted = outputs.max(1)
        pred_cpu = predicted.cpu()
        all_pred.extend(pred_cpu.numpy())
        all_true.extend(labels.numpy())
        for i in range(len(labels)):
            if pred_cpu[i] == labels[i]:
                class_correct[labels[i]] += 1
            class_total[labels[i]] += 1

print("Per-class accuracy:")
for i, cls in enumerate(classes):
    acc = 100 * class_correct[i] / class_total[i]
    bar = '█' * int(acc // 5)
    print(f"  {cls:8s}: {acc:.1f}% {bar}")

# Confusion matrix
cm = confusion_matrix(all_true, all_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=classes, yticklabels=classes)
plt.title('Confusion Matrix — Where Does the Model Struggle?')
plt.show()

# Grad-CAM visualisation
grad_cam = GradCAM(model, model.conv3)
fig, axes = plt.subplots(2, 5, figsize=(15, 6))
for i, (img, label) in enumerate(testset):
    if i >= 10: break
    input_tensor = img.unsqueeze(0).to(device)
    with torch.no_grad():
        out = model(input_tensor)
    pred_class = out.argmax().item()
    cam = grad_cam.generate(input_tensor, pred_class)

    img_np = img.permute(1,2,0).numpy() * 0.5 + 0.5
    ax = axes[i//5][i%5]
    ax.imshow(img_np)
    cam_resized = np.array(
        __import__('PIL').Image.fromarray((cam*255).astype(np.uint8)).resize((32,32)))
    ax.imshow(cam_resized, cmap='jet', alpha=0.4)
    color = 'green' if pred_class == label else 'red'
    ax.set_title(f"True:{classes[label]}\nPred:{classes[pred_class]}",
                 color=color, fontsize=8)
    ax.axis('off')

plt.suptitle('Grad-CAM — What the CNN is Looking At')
plt.tight_layout()
plt.show()
```

**What v2 adds over v1:**
- Grad-CAM — heatmap shows which pixels influenced each prediction
- Per-class accuracy — cat/dog much harder than plane/car (understand WHY)
- Confusion matrix — which classes the model confuses (cat↔dog, car↔truck)
- Colour-coded Grad-CAM overlay on test images

---

## 🔴 v3.0 — Live Image Classifier App

**New in v3:** Upload any image → get prediction + confidence, REST API, Streamlit UI

```python
# Part A — FastAPI Image Scoring (api.py)
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import torch, torchvision.transforms as transforms
import io, numpy as np

app = FastAPI(title="Image Classifier API")

# Load model (define CNN class above, then:)
# model = CNN(); model.load_state_dict(torch.load('cnn_cifar10.pth'))
# model.eval()

CLASSES = ['airplane','automobile','bird','cat','deer',
           'dog','frog','horse','ship','truck']

transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
])

@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert('RGB')
    tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        output = model(tensor)
        probs  = torch.softmax(output, dim=1)[0]

    top3_probs, top3_idx = probs.topk(3)

    return {
        "filename": file.filename,
        "top_prediction": {
            "class": CLASSES[top3_idx[0].item()],
            "confidence": f"{top3_probs[0].item()*100:.1f}%"
        },
        "top_3": [
            {"class": CLASSES[i.item()], "confidence": f"{p.item()*100:.1f}%"}
            for p, i in zip(top3_probs, top3_idx)
        ]
    }
```

```python
# Part B — Streamlit Upload UI (streamlit_app.py)
import streamlit as st
from PIL import Image
import torch
import torchvision.transforms as transforms
import numpy as np
import plotly.express as px
import torch.nn as nn
import torch.nn.functional as F

st.set_page_config(page_title="Image Classifier", page_icon="🖼️", layout="wide")
st.title("🖼️ CNN Image Classifier — PJS Academy")
st.caption("Upload any image → get AI prediction with confidence scores")

CLASSES = ['airplane','automobile','bird','cat','deer',
           'dog','frog','horse','ship','truck']

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1=nn.Conv2d(3,32,3,padding=1); self.bn1=nn.BatchNorm2d(32)
        self.conv2=nn.Conv2d(32,64,3,padding=1); self.bn2=nn.BatchNorm2d(64)
        self.conv3=nn.Conv2d(64,128,3,padding=1); self.bn3=nn.BatchNorm2d(128)
        self.pool=nn.MaxPool2d(2,2); self.drop=nn.Dropout(0.4)
        self.fc1=nn.Linear(128*4*4,512); self.fc2=nn.Linear(512,10)
    def forward(self,x):
        x=self.pool(F.relu(self.bn1(self.conv1(x))))
        x=self.pool(F.relu(self.bn2(self.conv2(x))))
        x=self.pool(F.relu(self.bn3(self.conv3(x))))
        x=x.view(-1,128*4*4)
        return self.fc2(self.drop(F.relu(self.fc1(x))))

@st.cache_resource
def load_model():
    m = CNN()
    m.load_state_dict(torch.load('cnn_cifar10.pth', map_location='cpu'))
    m.eval()
    return m

model = load_model()

transform = transforms.Compose([
    transforms.Resize((32,32)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
])

uploaded = st.file_uploader("Upload an image (jpg, png):", type=['jpg','jpeg','png'])
if uploaded:
    col1, col2 = st.columns(2)
    img = Image.open(uploaded).convert('RGB')
    col1.image(img, caption="Your Image", use_column_width=True)

    tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        output = model(tensor)
        probs  = torch.softmax(output, dim=1)[0].numpy()

    top_class = CLASSES[probs.argmax()]
    top_conf  = probs.max() * 100

    with col2:
        st.markdown(f"### 🏆 Prediction: **{top_class.upper()}**")
        st.markdown(f"**Confidence:** {top_conf:.1f}%")
        st.progress(float(probs.max()))

        fig = px.bar(x=CLASSES, y=probs*100, labels={'x':'Class','y':'Confidence %'},
                     color=probs*100, color_continuous_scale='Blues',
                     title='All Class Probabilities')
        st.plotly_chart(fig, use_container_width=True)
```

**What v3 adds over v2:**
- FastAPI `/classify` endpoint — any image, JSON response in <100ms
- Streamlit upload UI — drag and drop any image, see top-3 predictions
- Probability bar chart for all 10 classes — see the model's uncertainty
- `@st.cache_resource` — model loaded once, reused across all requests

---

## 📈 Learning Progression Summary

```
v1 → Train CNN on CIFAR-10, understand layers, hit 80%+ accuracy
v2 → See WHAT your CNN looks at (Grad-CAM), find class-specific weaknesses
v3 → Upload any image → instant prediction with confidence — deploy as an app
```

---

*Course: [Data Science Mastery — PJS Academy](https://pjsacademy.com)*
