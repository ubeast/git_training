"""Tested logic for the weekly rollup.

This is a plain module (no `# Databricks notebook source` header) so it can be
unit-tested with pytest in CI and imported by the notebook. Keep the real logic
here; keep the notebook thin (Module 11).
"""

from pyspark.sql import DataFrame, functions as F


def build_weekly_rollup(df: DataFrame) -> DataFrame:
    """Sum `amount` per `day_of_week`, ordered by day.

    Args:
        df: rows with at least `day_of_week` (int) and `amount` (numeric).

    Returns:
        One row per `day_of_week` with a `total_amount` column.
    """
    return (
        df.groupBy("day_of_week")
        .agg(F.sum("amount").alias("total_amount"))
        .orderBy("day_of_week")
    )
