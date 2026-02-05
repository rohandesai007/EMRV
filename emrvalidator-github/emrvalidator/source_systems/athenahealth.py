"""
ATHENAHEALTH source system rule set.
"""

from __future__ import annotations

from ..rules import RuleSet
from .common import build_ruleset

SYSTEM_KEY = "athenahealth"
DISPLAY = "ATHENAHEALTH"

REQUIRED_COLUMNS = [
    "patient_id",
    "mrn",
    "encounter_id",
    "service_date",
    "diagnosis_code",
    "procedure_code",
    "dob",
    "sex",
]

NOT_NULL_COLUMNS = ["patient_id", "mrn", "encounter_id", "diagnosis_code"]
UNIQUE_COLUMNS = ["encounter_id"]


def ruleset() -> RuleSet:
    return build_ruleset(DISPLAY, REQUIRED_COLUMNS, NOT_NULL_COLUMNS, UNIQUE_COLUMNS)
