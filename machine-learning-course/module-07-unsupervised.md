# Module 07 — Unsupervised Learning: Finding Hidden Structure

> No labels, no "right answer" — just data. The model discovers patterns on its own: groups, structure, compression.

---

## 7.1 What "Unsupervised" Means

You have features (X) but **no target (y)**. The goal isn't prediction — it's **understanding**: What natural groups exist? What are the main dimensions of variation? Which points are anomalies?

Two workhorses: **clustering** (grouping) and **dimensionality reduction** (compressing).

## 7.2 K-Means Clustering

Groups data into **k** clusters by repeatedly: assign each point to the nearest cluster centre, then move each centre to the average of its points — until stable.

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

X_scaled = StandardScaler().fit_transform(X)   # scaling is essential (distance-based)
km = KMeans(n_clusters=4, n_init=10, random_state=42)
labels = km.fit_predict(X_scaled)              # which cluster each point belongs to
```

**Choosing k — the Elbow Method:** plot within-cluster error (inertia) vs k; the "elbow" where it stops dropping sharply is a good k.
```python
inertias = [KMeans(k, n_init=10, random_state=42).fit(X_scaled).inertia_ for k in range(1,10)]
# plot inertias vs k, look for the elbow
```
Also check the **silhouette score** (−1 to 1; higher = better-separated clusters).

> **Always scale before K-Means** — otherwise the largest-scale feature dominates the distances.

## 7.3 Real Use: Customer Segmentation

The classic business application — group customers by behaviour, then treat each segment differently:
```python
# Features: recency, frequency, monetary (RFM)
km = KMeans(n_clusters=4, n_init=10, random_state=42)
df['segment'] = km.fit_predict(StandardScaler().fit_transform(df[['recency','frequency','monetary']]))
# Now: "high-value loyal", "at-risk", "new", "bargain" → tailored marketing
```

## 7.4 Other Clustering Methods

- **Hierarchical clustering** — builds a tree of nested clusters (dendrogram); no need to pick k upfront.
- **DBSCAN** — density-based; finds arbitrary shapes and labels outliers as noise. Great when clusters aren't round and you don't know k.
```python
from sklearn.cluster import DBSCAN
DBSCAN(eps=0.5, min_samples=5).fit_predict(X_scaled)   # -1 = noise/outlier
```

## 7.5 Dimensionality Reduction — PCA

Real data has many features, often correlated. **PCA (Principal Component Analysis)** finds new axes ("components") that capture the most variation, letting you keep the signal with fewer dimensions.

Why reduce dimensions?
- **Visualization** — squash 50 features to 2 for a scatter plot.
- **Speed & noise** — fewer features = faster training, less overfitting.
- **Remove redundancy** — combine correlated features.

```python
from sklearn.decomposition import PCA
pca = PCA(n_components=2)               # or n_components=0.95 to keep 95% of variance
X_reduced = pca.fit_transform(X_scaled)
print(pca.explained_variance_ratio_)   # how much variance each component captures
```
> PCA components are combinations of original features — powerful but less interpretable. Scale first.

## 7.6 t-SNE / UMAP — visualization only

For seeing high-dimensional data in 2D (great for images, embeddings). They preserve *local* structure beautifully but distances/sizes aren't meaningful — **use for plots, not as model inputs.**
```python
from sklearn.manifold import TSNE
X_2d = TSNE(n_components=2, perplexity=30).fit_transform(X_scaled)
```

## 7.7 Anomaly Detection

Find the weird points — fraud, defects, intrusions. Unsupervised because anomalies are rare and often unlabelled.
```python
from sklearn.ensemble import IsolationForest
iso = IsolationForest(contamination=0.02, random_state=42)
outliers = iso.fit_predict(X_scaled)   # -1 = anomaly, 1 = normal
```

## 7.8 Evaluating Unsupervised Models (the hard part)

No labels = no accuracy. Instead:
- **Silhouette score / Davies–Bouldin** for cluster quality.
- **Explained variance** for PCA.
- **Business validation** — do the segments make sense and drive action? Ultimately, usefulness beats any metric.

---

## ✅ Key Takeaways
1. Unsupervised learning finds **structure without labels** — clustering and dimensionality reduction.
2. **K-Means** groups by nearest centre; **scale first**, pick k with the elbow/silhouette.
3. **DBSCAN/hierarchical** handle non-round clusters and unknown k.
4. **PCA** compresses correlated features while keeping variance — for speed, denoising, and visualization.
5. **t-SNE/UMAP** are for plots only, not model inputs.
6. Evaluate with silhouette/explained variance — but **business usefulness** is the real test.

## 🏋️ Exercises
1. Cluster a dataset with K-Means; use the elbow method to choose k; describe each cluster.
2. Run PCA to 2 components and scatter-plot; how much variance is retained?
3. Use IsolationForest to flag the top 2% anomalies and inspect them.
4. Compare K-Means vs DBSCAN on data with non-round clusters.

## 🛠️ Mini-Project
Segment mall/retail customers with K-Means on RFM features. Choose k, profile each segment, and write a one-line marketing action per segment. Bonus: visualize with PCA.

**Next:** [Module 08 — Tuning & Selection →](module-08-tuning.md)

---

*🤖 Machine Learning Mastery — [PJ's Academy](https://pjsacademy.com)*
