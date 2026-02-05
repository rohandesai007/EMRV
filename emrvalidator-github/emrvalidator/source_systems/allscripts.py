"""
ALLSCRIPTS source system rule set.
"""

from __future__ import annotations

from ..rules import RuleSet
from .common import build_ruleset

SYSTEM_KEY = "allscripts"
DISPLAY = "ALLSCRIPTS"

REQUIRED_COLUMNS = [
    "patient_id",
    "mrn",
    "visit_id",
    "service_date",
    "diagnosis_code",
    "procedure_code",
    "dob",
    "gender",
]

NOT_NULL_COLUMNS = ["patient_id", "mrn", "visit_id", "diagnosis_code"]
UNIQUE_COLUMNS = ["visit_id"]

COLUMN_ALIASES = {
    "patient_id": ["person_id", "pat_id", "patientid"],
    "mrn": ["medical_record_num", "medical_record_number", "mrn_id"],
    "visit_id": ["encounter_id", "enc_id"],
    "service_date": ["admit_date", "admit_dt", "service_dt"],
    "diagnosis_code": ["icd10_code", "icd_code", "dx_code"],
    "procedure_code": ["cpt_code", "proc_code"],
    "dob": ["birth_date", "date_of_birth"],
    "gender": ["sex"],
}


def ruleset() -> RuleSet:
    return build_ruleset(DISPLAY, REQUIRED_COLUMNS, NOT_NULL_COLUMNS, UNIQUE_COLUMNS)
