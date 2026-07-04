# Module 04 — Classification: Predicting Categories

> Predicting *which class* something belongs to — spam/not-spam, disease/healthy, which digit. The most common ML task in industry.

---

## 4.1 Regression vs Classification

- Regression predicts a **number** (₹45,000).
- Classification predicts a **category** (spam / not spam), usually via a **probability** (0.92 → spam).

The output is a class label, and often a probability behind it that you threshold (e.g., ≥ 0.5 → positive).

## 4.2 Logistic Regression (don't let the name fool you — it's classification)

It predicts a **probability** by squashing a linear score through the **sigmoid** function (an S-curve that maps any number to 0–1):
```
score = w·x + b   →   probability = sigmoid(score) = 1 / (1 + e^-score)
```
If probability ≥ 0.5 → class 1, else class 0.

```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
pred   = model.predict(X_test)            # class labels
proba  = model.predict_proba(X_test)[:,1] # probability of class 1
```
> Great interpretable baseline for any classification problem. Scale features first.

## 4.3 k-Nearest Neighbours (kNN) — "you are who your neighbours are"

To classify a new point, look at the **k closest** training points and take the majority vote.
```python
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
```
- **Must scale features** (it's distance-based).
- `k` too small → noisy/overfit; too large → oversmoothed. Tune it.
- Simple and intuitive, but slow on big data (compares to everything).

## 4.4 Naive Bayes — fast, great for text

Uses probability (Bayes' theorem) and "naively" assumes features are independent. Surprisingly strong for **text/spam classification**.
```python
from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB().fit(X_train, y_train)  # X often word counts / TF-IDF
```
Blazing fast, works well with many features (words). A classic spam-filter engine.

## 4.5 Decision Trees — human-readable rules

A tree of yes/no questions that split the data toward pure groups:
```
Is income > 50k?
├─ Yes → Is age > 30? → ...
└─ No  → Class: Reject
```
```python
from sklearn.tree import DecisionTreeClassifier
tree = DecisionTreeClassifier(max_depth=4, random_state=42)
tree.fit(X_train, y_train)
```
- **No scaling needed**; handles non-linear patterns; easy to explain.
- **Overfits badly if unpruned** — always limit `max_depth` / `min_samples_leaf`.
- Single trees are unstable → we fix this with **ensembles** (Module 05).

```python
# See the rules
from sklearn.tree import export_text
print(export_text(tree, feature_names=list(X.columns)))
```

## 4.6 Evaluating Classification (accuracy is a trap)

**Accuracy** = % correct. But on imbalanced data it lies: if 99% of transactions are legit, a model that says "always legit" is 99% accurate and 100% useless.

Use the **confusion matrix** and its metrics:

```
                Predicted +   Predicted −
Actual +           TP            FN
Actual −           FP            TN
```
- **Precision** = TP / (TP + FP) — "of those I flagged positive, how many really are?" (cost of false alarms)
- **Recall** = TP / (TP + FN) — "of all real positives, how many did I catch?" (cost of misses)
- **F1** = harmonic mean of precision & recall — one balanced number.
- **ROC-AUC** — ranks how well the model separates classes across all thresholds (0.5 = random, 1.0 = perfect).

```python
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred))
print("ROC-AUC:", roc_auc_score(y_test, proba))
```

## 4.7 Precision vs Recall — a business decision

You usually trade one for the other by moving the probability **threshold**:
- **Cancer screening** → maximise **recall** (never miss a case; false alarms are acceptable).
- **Spam filter** → maximise **precision** (don't send real mail to spam; a little spam getting through is OK).

```python
# Custom threshold instead of the default 0.5
pred_custom = (proba >= 0.3).astype(int)   # lower threshold → higher recall
```

## 4.8 Handling Class Imbalance

When one class is rare (fraud, disease):
- `class_weight='balanced'` in the model (penalize mistakes on the rare class more).
- **Resampling** — oversample the minority (SMOTE) or undersample the majority.
- Evaluate with **PR-AUC / F1 / recall**, never plain accuracy.

```python
LogisticRegression(class_weight='balanced', max_iter=1000)
```

## 4.9 Choosing a Classifier (starting map)

- **Interpretable baseline** → Logistic Regression.
- **Text** → Naive Bayes.
- **Small, need explanation** → Decision Tree.
- **Best accuracy on tabular data** → ensembles (Module 05) — usually the winner.

Start simple, measure, then upgrade.

---

## ✅ Key Takeaways
1. Classification predicts a **category**, usually via a **probability** you threshold.
2. **Logistic Regression** = sigmoid over a linear score; strong interpretable baseline.
3. **kNN** (scale it!), **Naive Bayes** (text), **Decision Trees** (readable, limit depth).
4. **Accuracy lies on imbalanced data** — use the **confusion matrix**, precision, recall, F1, ROC-AUC.
5. Trade **precision vs recall** by the threshold, based on business cost.
6. Handle **imbalance** with class weights / resampling and the right metrics.

## 🏋️ Exercises
1. Train Logistic Regression + a Decision Tree on the same data; compare F1 and ROC-AUC.
2. Print a confusion matrix and explain each cell (TP/FP/FN/TN) in words.
3. Lower the threshold to 0.3 and describe what happens to precision vs recall.
4. On an imbalanced dataset, compare accuracy vs F1 — show why accuracy misleads.

## 🛠️ Mini-Project
Build a churn classifier (Telco dataset). Logistic baseline → tune threshold for the business goal → handle imbalance with `class_weight='balanced'`. Report precision, recall, F1, and which errors cost more.

**Next:** [Module 05 — Ensembles →](module-05-ensembles.md)

---

*🤖 Machine Learning Mastery — [PJ's Academy](https://pjsacademy.com)*
