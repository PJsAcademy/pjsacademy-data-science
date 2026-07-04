# ❄️ Snowflake Project 14 — dbt + Snowflake Transformations (Advanced)

**What you build:** a production ELT project with dbt — staging → marts, with tests, docs, and an incremental model. dbt is the industry-standard transformation tool for Snowflake.

> dbt uses files (not a single script), so this project is a folder structure. Install: `pip install dbt-snowflake`.

## 1) Connect dbt to Snowflake — `~/.dbt/profiles.yml`
```yaml
pjs_academy:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "<your_account>"
      user: "<your_user>"
      password: "<your_password>"   # or authenticator/private key
      role: SYSADMIN
      warehouse: ANALYTICS_WH
      database: ANALYTICS
      schema: DBT_DEV
      threads: 4
```

## 2) Project layout
```
pjs_dbt/
├── dbt_project.yml
├── models/
│   ├── staging/
│   │   ├── stg_orders.sql
│   │   └── schema.yml         # tests + docs
│   └── marts/
│       ├── fct_daily_revenue.sql
│       └── dim_customers.sql
```

## 3) `dbt_project.yml`
```yaml
name: 'pjs_dbt'
version: '1.0'
profile: 'pjs_academy'
models:
  pjs_dbt:
    staging:
      +materialized: view
    marts:
      +materialized: table
```

## 4) Staging model — `models/staging/stg_orders.sql`
```sql
-- Clean + standardise raw orders (a view)
select
    order_id,
    trim(customer)        as customer,
    lower(email)          as email,
    abs(amount)           as amount,
    order_ts::date        as order_date
from {{ source('raw', 'orders') }}
where amount is not null
```

## 5) Tests + docs — `models/staging/schema.yml`
```yaml
version: 2
sources:
  - name: raw
    database: RAW
    tables: [{ name: orders }]
models:
  - name: stg_orders
    description: "Cleaned orders, one row per order."
    columns:
      - name: order_id
        tests: [unique, not_null]      # dbt runs these as SQL assertions
      - name: amount
        tests: [not_null]
```

## 6) Mart model — `models/marts/fct_daily_revenue.sql`
```sql
select
    order_date,
    count(*)      as orders,
    sum(amount)   as revenue
from {{ ref('stg_orders') }}          -- ref() builds the DAG
group by order_date
```

## 7) Incremental model (only process NEW rows) — big-table pattern
```sql
{{ config(materialized='incremental', unique_key='order_id') }}
select * from {{ ref('stg_orders') }}
{% if is_incremental() %}
  where order_date > (select max(order_date) from {{ this }})
{% endif %}
```

## 8) Run it
```bash
dbt run          # build all models (staging views + mart tables)
dbt test         # run the data tests (unique, not_null, ...)
dbt docs generate && dbt docs serve   # auto-generated documentation + DAG
```

## What you learned
Layered ELT (staging → marts), `source()`/`ref()` for a dependency DAG, data tests, incremental models, and auto docs — the modern data stack on Snowflake.

**Next:** Project 15 — CDC Data Vault.

---
*❄️ Snowflake Mastery — [PJ's Academy](https://pjsacademy.com)*
