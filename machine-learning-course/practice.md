# 🧠 Machine Learning — Practice & Quiz Bank

Test your understanding. Concept quizzes (with answers) + coding drills, organized by module. Do these before moving between modules — they catch gaps.

---

## 📝 Concept Quiz (40 questions, answers at the bottom)

### Module 1–2: Foundations & Data
1. Is predicting a customer's age regression or classification?
2. What's the difference between a parameter and a hyperparameter?
3. Why must you fit a scaler on the training set only?
4. What is data leakage, in one sentence?
5. When should you one-hot encode vs ordinal encode?
6. Which models don't need feature scaling?
7. What does `df.isnull().sum()` tell you?
8. Overfitting: high or low training accuracy? High or low test accuracy?

### Module 3–4: Regression & Classification
9. What does R² = 0.8 mean?
10. Why square the errors in MSE?
11. What does Lasso do that Ridge doesn't?
12. What function turns a linear score into a 0–1 probability?
13. Why is accuracy misleading on imbalanced data?
14. Define precision and recall in one line each.
15. For cancer screening, do you optimize precision or recall? Why?
16. What does a confusion matrix show?

### Module 5–6: Ensembles & Evaluation
17. Bagging reduces ___; boosting reduces ___.
18. How does Random Forest create diversity among trees?
19. In XGBoost, what does a lower learning_rate require more of?
20. What is early stopping and why use it?
21. What is k-fold cross-validation?
22. Why use StratifiedKFold for classification?
23. Learning curve: train high, val low, big gap → which problem?
24. Name two ways test information can leak into training.

### Module 7–8: Unsupervised & Tuning
25. What does K-Means minimize?
26. How does the elbow method choose k?
27. Why must you scale before K-Means and PCA?
28. What does PCA do?
29. When is t-SNE appropriate — model input or visualization?
30. Grid search vs random search — when prefer random?
31. Why wrap preprocessing + model in a Pipeline for tuning?
32. What usually beats hyperparameter tuning for improving a model?

### Module 9–10: Neural Nets & Production
33. Without activation functions, what does a deep network collapse into?
34. What does dropout do?
35. Which optimizer is the common default?
36. For tabular data, what often beats neural nets?
37. Why save the whole pipeline, not just the model?
38. What is data drift vs concept drift?
39. Name two things to monitor for a production model.
40. What does SHAP help you do?

---

## 💻 Coding Drills
1. Load any dataset, do a full train/test split, and train a baseline model — report the right metric.
2. Build a `ColumnTransformer` that imputes + scales numerics and one-hots categoricals.
3. Compare Ridge (`alpha=0.1,1,10`) and plot coefficient shrinkage.
4. Train Logistic Regression + XGBoost on the same classification data; compare ROC-AUC.
5. Run 5-fold CV and report mean ± std.
6. Cluster a dataset with K-Means, choose k via elbow, and profile the clusters.
7. Tune XGBoost with RandomizedSearchCV inside a Pipeline.
8. Build + train a small Keras network; plot train vs validation loss.
9. Save a pipeline, reload it, and serve one prediction via FastAPI.
10. Use SHAP to explain a single prediction.

---

## ✅ Quiz Answers
1. Regression. 2. Parameters are learned; hyperparameters you set before training. 3. Fitting on all data leaks test info → inflated scores. 4. Test information sneaking into training. 5. One-hot for unordered categories, ordinal for ordered. 6. Tree-based (RF, XGBoost, decision trees). 7. Missing values per column. 8. High train, low test. 9. The model explains 80% of the target's variance. 10. So + and − errors don't cancel and big errors are punished more. 11. Lasso can zero out weights → feature selection. 12. Sigmoid. 13. A model predicting only the majority class scores high accuracy while being useless. 14. Precision = of predicted positives, how many are correct; Recall = of actual positives, how many were caught. 15. Recall — never miss a real case; false alarms are acceptable. 16. TP/FP/FN/TN — where the model is right and wrong. 17. variance; bias. 18. Random rows (bootstrap) + random feature subsets per split. 19. More trees (n_estimators). 20. Stop adding trees when val performance stops improving — prevents overfitting/saves time. 21. Split into k folds, train on k−1, test on 1, rotate, average. 22. Keeps class balance in each fold. 23. Overfitting (high variance). 24. Scaling before split; feature engineering using target stats over all data (also: shuffling time series, duplicate rows). 25. Within-cluster sum of squared distances (inertia). 26. The k where inertia stops dropping sharply (the "elbow"). 27. They're distance/variance-based; unscaled large features dominate. 28. Finds new axes capturing max variance → compress features. 29. Visualization only. 30. Large hyperparameter spaces. 31. So preprocessing is re-fit inside each CV fold → no leakage. 32. Better features / feature engineering. 33. A single linear model. 34. Randomly disables neurons during training to reduce overfitting. 35. Adam. 36. XGBoost/LightGBM. 37. Inference must apply identical preprocessing. 38. Data drift = input distribution shifts; concept drift = the input→output relationship changes. 39. Model metrics, data health/drift, latency, business KPI (any two). 40. Explain why the model made a prediction (feature contributions).

---

**Score yourself:** 32+/40 = strong. Below 24 → revisit the flagged modules before the projects.

*🤖 Machine Learning Mastery — [PJ's Academy](https://pjsacademy.com)*
