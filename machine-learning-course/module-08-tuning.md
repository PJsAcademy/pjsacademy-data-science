# Module 08 — Feature Selection, Tuning & Pipelines

> Turning a decent model into the best it can be — systematically, not by guessing.

---

## 8.1 Feature Selection — less is often more

Too many features → slower training, overfitting, noise. Keeping the useful ones helps.

**Methods:**
```python
# 1. Filter: correlation / statistical tests
from sklearn.feature_selection import SelectKBest, f_classif
X_best = SelectKBest(f_classif, k=10).fit_transform(X, y)

# 2. Model-based: importance from a tree/Lasso
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier
sel = SelectFromModel(RandomForestClassifier(n_estimators=200)).fit(X, y)

# 3. Recursive Feature Elimination (RFE): drop weakest, repeat
from sklearn.feature_selection import RFE
RFE(estimator=LogisticRegression(), n_features_to_select=10).fit(X, y)
```
Also just **use feature importances** (Module 05) or **Lasso** (Module 03) to drop dead weight.

## 8.2 Hyperparameters vs Parameters (reminder)

- **Parameters** — learned during training (weights, splits). You don't set these.
- **Hyperparameters** — you choose *before* training (tree depth, learning rate, k, alpha). **Tuning** = finding the best combination.

## 8.3 Grid Search — try every combination

```python
from sklearn.model_selection import GridSearchCV
import xgboost as xgb

param_grid = {
    'n_estimators': [200, 400],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.05, 0.1],
}
grid = GridSearchCV(xgb.XGBClassifier(random_state=42),
                    param_grid, cv=5, scoring='f1', n_jobs=-1)
grid.fit(X_train, y_train)
print(grid.best_params_, grid.best_score_)
best = grid.best_estimator_
```
Thorough but explodes combinatorially (2×3×2 = 12 fits × 5 folds = 60 trainings).

## 8.4 Random Search — smarter for big spaces

Samples random combinations — usually finds near-best far faster than grid search when there are many hyperparameters.
```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

dist = {'n_estimators': randint(100, 600),
        'max_depth': randint(3, 10),
        'learning_rate': uniform(0.01, 0.2)}
rs = RandomizedSearchCV(xgb.XGBClassifier(random_state=42), dist,
                        n_iter=30, cv=5, scoring='f1', n_jobs=-1, random_state=42)
rs.fit(X_train, y_train)
```

## 8.5 Bayesian Optimization — the pro tool

Uses past results to intelligently pick the next combination to try (Optuna). Finds better params in fewer trials — the modern standard.
```python
import optuna
def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 600),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
    }
    model = xgb.XGBClassifier(**params, random_state=42)
    return cross_val_score(model, X_train, y_train, cv=5, scoring='f1').mean()

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=40)
print(study.best_params)
```

## 8.6 Tune the Right Things

Don't tune everything — focus on the hyperparameters that matter most per model:
- **XGBoost/LightGBM:** `learning_rate`, `n_estimators`, `max_depth`, then subsampling/regularization.
- **Random Forest:** `n_estimators` (more is safe), `max_features`, `max_depth`.
- **kNN:** `n_neighbors`.
- **SVM:** `C`, `gamma`, `kernel`.
- **Regularized linear:** `alpha`.

## 8.7 Pipelines — tune preprocessing + model together

Wrap preprocessing and model in one Pipeline so cross-validation applies preprocessing **inside each fold** (no leakage):
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

pipe = Pipeline([('scaler', StandardScaler()),
                 ('model', LogisticRegression(max_iter=1000))])

param_grid = {'model__C': [0.1, 1, 10]}    # note the model__ prefix
grid = GridSearchCV(pipe, param_grid, cv=5).fit(X_train, y_train)
```
> This is the correct, leakage-free way to tune — the scaler is re-fit on each fold's training portion only.

## 8.8 Practical Tuning Workflow

```
1. Get a working baseline (default hyperparameters).
2. Fix data/features FIRST — feature engineering beats tuning.
3. Coarse random/Bayesian search over key hyperparameters.
4. Narrow the ranges around the best, search again.
5. Validate the final choice on the untouched test set.
```
> ⚠️ Tuning gives diminishing returns. A 2% gain from tuning is nice; a 10% gain from a better feature is the real win. Spend effort where it pays.

---

## ✅ Key Takeaways
1. **Feature selection** (filter, model-based, RFE) cuts noise and overfitting.
2. **Tuning** = searching hyperparameters: **grid** (small spaces), **random** (bigger), **Bayesian/Optuna** (best).
3. Tune only the **high-impact hyperparameters** per model.
4. Use **Pipelines** so preprocessing is tuned/CV'd without leakage.
5. **Fix features before you tune** — engineering usually beats optimization.
6. Confirm the final model on the **untouched test set**.

## 🏋️ Exercises
1. Run GridSearchCV over 2–3 hyperparameters; report best params and CV score.
2. Compare grid vs random search speed and result on the same model.
3. Wrap a scaler + model in a Pipeline and tune with the `model__` prefix.
4. (Bonus) Use Optuna for 30 trials on XGBoost; beat your grid-search score.

## 🛠️ Mini-Project
Take any earlier project model and run a full tuning workflow: baseline → feature selection → Bayesian search in a Pipeline → final test-set evaluation. Document the gain at each step.

**Next:** [Module 09 — Neural Networks →](module-09-neural-nets.md)

---

*🤖 Machine Learning Mastery — [PJ's Academy](https://pjsacademy.com)*
