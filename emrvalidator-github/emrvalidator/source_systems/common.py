"""
Shared helpers for source-system rule sets.
"""

from __future__ import annotations

from typing import List

import pandas as pd

from ..rules import RuleSet


def _require_columns(columns: List[str]):
    def validate(df: pd.DataFrame, **kwargs):
        missing = [col for col in columns if col not in df.columns]
        passed = len(missing) == 0
        message = "All required columns present" if passed else "Missing required columns: " + ", ".join(missing)
        return passed, message, {"missing_columns": missing}

    return validate


def _non_null(column: str, mostly: float = 0.99):
    def validate(df: pd.DataFrame, **kwargs):
        if column not in df.columns:
            return False, f"Column '{column}' not found", {}
        non_null_pct = float(df[column].notna().mean())
        passed = non_null_pct >= mostly
        return (
            passed,
            f"Non-null '{column}': {non_null_pct*100:.2f}% (expected {mostly*100}%)",
            {
                "column": column,
                "non_null_percentage": round(non_null_pct * 100, 2),
                "null_count": int(df[column].isna().sum()),
            },
        )

    return validate


def _mostly_unique(column: str, mostly: float = 0.99):
    def validate(df: pd.DataFrame, **kwargs):
        if column not in df.columns:
            return False, f"Column '{column}' not found", {}
        unique_pct = float(df[column].nunique(dropna=True) / max(len(df), 1))
        passed = unique_pct >= mostly
        return (
            passed,
            f"Unique '{column}': {unique_pct*100:.2f}% (expected {mostly*100}%)",
            {
                "column": column,
                "unique_percentage": round(unique_pct * 100, 2),
                "duplicate_count": int(len(df) - df[column].nunique(dropna=True)),
            },
        )

    return validate


def build_ruleset(
    display: str,
    required_columns: List[str],
    not_null_columns: List[str],
    unique_columns: List[str],
) -> RuleSet:
    ruleset = RuleSet(
        f"{display} Export",
        f"Baseline validation rules for {display} exports",
    )

    ruleset.create_rule(
        "required_columns",
        "Required columns present",
        _require_columns(required_columns),
    )

    for column in not_null_columns:
        ruleset.create_rule(
            f"not_null_{column}",
            f"'{column}' must be mostly non-null",
            _non_null(column),
        )

    for column in unique_columns:
        ruleset.create_rule(
            f"unique_{column}",
            f"'{column}' should be mostly unique",
            _mostly_unique(column),
            critical=False,
        )

    return ruleset
