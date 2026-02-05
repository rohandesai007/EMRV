"""
EPIC source system rule set.
"""

from __future__ import annotations

from ..rules import RuleSet
from .common import build_ruleset

SYSTEM_KEY = "epic"
DISPLAY = "EPIC"

REQUIRED_COLUMNS = [
    "patient_id",
    "mrn",
    "encounter_id",
    "admit_datetime",
    "discharge_datetime",
    "diagnosis_code",
    "procedure_code",
    "dob",
    "sex",
]

NOT_NULL_COLUMNS = ["patient_id", "mrn", "encounter_id", "diagnosis_code"]
UNIQUE_COLUMNS = ["encounter_id"]

COLUMN_ALIASES = {
    "patient_id": ["person_id", "pat_id", "patientid"],
    "mrn": ["medical_record_num", "medical_record_number", "mrn_id"],
    "encounter_id": ["visit_id", "enc_id"],
    "admit_datetime": ["admit_dt", "admission_datetime", "admission_date"],
    "discharge_datetime": ["discharge_dt", "discharge_date"],
    "diagnosis_code": ["icd10_code", "icd_code", "dx_code"],
    "procedure_code": ["cpt_code", "proc_code"],
    "dob": ["birth_date", "date_of_birth"],
    "sex": ["gender"],
}


def ruleset() -> RuleSet:
    return build_ruleset(DISPLAY, REQUIRED_COLUMNS, NOT_NULL_COLUMNS, UNIQUE_COLUMNS)
