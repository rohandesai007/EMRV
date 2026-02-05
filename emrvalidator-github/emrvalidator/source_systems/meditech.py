"""
MEDITECH source system rule set.
"""

from __future__ import annotations

from ..rules import RuleSet
from .common import build_ruleset

SYSTEM_KEY = "meditech"
DISPLAY = "MEDITECH"

REQUIRED_COLUMNS = [
    "patient_id",
    "mrn",
    "visit_id",
    "admit_date",
    "discharge_date",
    "icd_code",
    "cpt_code",
    "dob",
    "gender",
]

NOT_NULL_COLUMNS = ["patient_id", "mrn", "visit_id", "icd_code"]
UNIQUE_COLUMNS = ["visit_id"]

COLUMN_ALIASES = {
    "patient_id": ["person_id", "pat_id", "patientid"],
    "mrn": ["medical_record_num", "medical_record_number", "mrn_id"],
    "visit_id": ["encounter_id", "enc_id"],
    "admit_date": ["admit_dt", "admit_datetime", "admission_date"],
    "discharge_date": ["discharge_dt", "discharge_datetime"],
    "icd_code": ["icd10_code", "diagnosis_code", "dx_code"],
    "cpt_code": ["procedure_code", "proc_code"],
    "dob": ["birth_date", "date_of_birth"],
    "gender": ["sex"],
}


def ruleset() -> RuleSet:
    return build_ruleset(DISPLAY, REQUIRED_COLUMNS, NOT_NULL_COLUMNS, UNIQUE_COLUMNS)
