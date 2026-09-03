# Databricks notebook source
# MAGIC %md
# MAGIC # Weekly rollup (Exercise 06 sample)
# MAGIC Thin notebook: reads a parameter, calls a tested module, writes a table.

# COMMAND ----------

dbutils.widgets.text("catalog", "main_dev")
catalog = dbutils.widgets.get("catalog")
print(f"Running weekly rollup against catalog: {catalog}")

# COMMAND ----------

# The Git folder / bundle root is on sys.path, so this import works.
from src.rollup_lib import build_weekly_rollup

# COMMAND ----------

source = spark.range(0, 100).selectExpr(
    "id",
    "id % 7 as day_of_week",
    "rand() * 100 as amount",
)

weekly = build_weekly_rollup(source)
display(weekly)

# COMMAND ----------

# In a real job you'd write to Unity Catalog, e.g.:
#   weekly.write.mode("overwrite").saveAsTable(f"{catalog}.sandbox.weekly_rollup")
print("done")
