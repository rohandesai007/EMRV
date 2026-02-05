"""
CERNER source system rule set.
"""

from __future__ import annotations

from ..rules import RuleSet
from .common import build_ruleset

SYSTEM_KEY = "cerner"
DISPLAY = "CERNER"

REQUIRED_COLUMNS = [
    "person_id",
    "mrn",
    "encounter_id",
    "admit_dt",
    "discharge_dt",
    "icd10_code",
    "cpt_code",
    "birth_date",
    "sex",
]

NOT_NULL_COLUMNS = ["person_id", "mrn", "encounter_id", "icd10_code"]
UNIQUE_COLUMNS = ["encounter_id"]


def ruleset() -> RuleSet:
    return build_ruleset(DISPLAY, REQUIRED_COLUMNS, NOT_NULL_COLUMNS, UNIQUE_COLUMNS)
