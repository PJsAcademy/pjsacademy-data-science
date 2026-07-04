# ============================================================================
# PJ's Academy · Snowflake Project 10 — In-Warehouse ML with Snowpark (Advanced)
# ----------------------------------------------------------------------------
# WHAT YOU BUILD: train a churn model, register it, and deploy it as a
#   Python UDF so anyone can score customers directly in SQL — data never
#   leaves Snowflake.
# HOW TO RUN: in a Snowflake Notebook (recommended) or locally with a
#   Snowpark session. Requires: snowflake-snowpark-python, scikit-learn.
#   pip install "snowflake-snowpark-python[pandas]" scikit-learn
# ============================================================================

from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import pandas as pd

# 1) Connect --------------------------------------------------------------
# In a Snowflake Notebook, a session already exists: use get_active_session().
# Locally, fill in your account details:
CONNECTION = {
    "account":   "<your_account>",
    "user":      "<your_user>",
    "password":  "<your_password>",   # or use key-pair auth in production
    "role":      "SYSADMIN",
    "warehouse": "ANALYTICS_WH",
    "database":  "ML_DEMO",
    "schema":    "PUBLIC",
}

def get_session():
    try:                                   # inside a Snowflake Notebook
        from snowflake.snowpark.context import get_active_session
        return get_active_session()
    except Exception:                      # local
        return Session.builder.configs(CONNECTION).create()

session = get_session()
session.sql("CREATE DATABASE IF NOT EXISTS ML_DEMO").collect()
session.sql("CREATE SCHEMA IF NOT EXISTS ML_DEMO.PUBLIC").collect()
session.sql("CREATE STAGE IF NOT EXISTS ML_DEMO.PUBLIC.ML_STAGE").collect()
session.use_database("ML_DEMO"); session.use_schema("PUBLIC")

# 2) Create sample training data in Snowflake -----------------------------
train_pd = pd.DataFrame({
    "tenure":         [1, 24, 5, 40, 3, 60, 12, 2, 36, 8],
    "monthly":        [80, 20, 95, 25, 90, 30, 55, 99, 22, 70],
    "contract":       [0, 2, 0, 2, 0, 2, 1, 0, 2, 1],   # 0=monthly,1=1yr,2=2yr
    "churn":          [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
})
session.create_dataframe(train_pd).write.mode("overwrite").save_as_table("customers_train")
print("Training table rows:", session.table("customers_train").count())

# 3) Train a model (scikit-learn, on data pulled once) --------------------
df = session.table("customers_train").to_pandas()
X = df[["TENURE", "MONTHLY", "CONTRACT"]]
y = df["CHURN"]

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42).fit(X, y)
print("Train accuracy:", model.score(X, y))

# 4) Deploy the model as a Python UDF that runs INSIDE Snowflake ----------
#    sproc/udf registration uploads the model to the stage and makes it
#    callable from SQL. No data ever leaves the platform.
from snowflake.snowpark.functions import udf
from snowflake.snowpark.types import IntegerType, FloatType
import joblib, os

# Save + upload the trained model to the stage
joblib.dump(model, "/tmp/churn_model.joblib")
session.file.put("/tmp/churn_model.joblib", "@ML_STAGE",
                 auto_compress=False, overwrite=True)

@udf(name="predict_churn", is_permanent=True, replace=True,
     stage_location="@ML_STAGE",
     packages=["scikit-learn", "joblib", "cachetools"],
     imports=["@ML_STAGE/churn_model.joblib"])
def predict_churn(tenure: int, monthly: float, contract: int) -> float:
    import sys, joblib, cachetools
    # cache the model load across invocations for speed
    @cachetools.cached(cache={})
    def load_model():
        import_dir = sys._xoptions["snowflake_import_directory"]
        return joblib.load(import_dir + "churn_model.joblib")
    m = load_model()
    return float(m.predict_proba([[tenure, monthly, contract]])[0][1])

print("UDF 'predict_churn' deployed.")

# 5) Score customers directly in SQL -------------------------------------
session.sql("""
    CREATE OR REPLACE TABLE customers_live AS
    SELECT * FROM VALUES
      (101, 2, 95, 0), (102, 48, 20, 2), (103, 6, 85, 0)
    AS t(customer_id, tenure, monthly, contract)
""").collect()

result = session.sql("""
    SELECT customer_id, tenure, monthly, contract,
           ROUND(predict_churn(tenure, monthly, contract), 3) AS churn_risk,
           CASE WHEN predict_churn(tenure, monthly, contract) > 0.5
                THEN 'HIGH' ELSE 'LOW' END AS risk_tier
    FROM customers_live
    ORDER BY churn_risk DESC
""")
result.show()

# ============================================================================
# WHAT YOU LEARNED: Snowpark sessions, saving a model to a stage, deploying a
# Python UDF (with imports + packages), and calling ML from pure SQL.
# THE BIG IDEA: analysts now run ML predictions with a SQL function — zero
# data egress, no separate ML server.
# NEXT: Project 20 — the end-to-end data platform capstone.
# ============================================================================
