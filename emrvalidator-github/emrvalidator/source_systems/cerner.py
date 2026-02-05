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

COLUMN_ALIASES = {
    "person_id": ["patient_id", "pat_id", "patientid"],
    "mrn": ["medical_record_num", "medical_record_number", "mrn_id"],
    "encounter_id": ["visit_id", "enc_id"],
    "admit_dt": ["admit_datetime", "admission_date", "admission_datetime"],
    "discharge_dt": ["discharge_datetime", "discharge_date"],
    "icd10_code": ["diagnosis_code", "icd_code", "dx_code"],
    "cpt_code": ["procedure_code", "proc_code"],
    "birth_date": ["dob", "date_of_birth"],
    "sex": ["gender"],
}


def ruleset() -> RuleSet:
    return build_ruleset(DISPLAY, REQUIRED_COLUMNS, NOT_NULL_COLUMNS, UNIQUE_COLUMNS)
