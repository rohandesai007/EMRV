"""
Source-system rule sets for common EMR exports.
"""

from __future__ import annotations

from typing import List

import pandas as pd

from ..rules import RuleSet
from . import epic, cerner, meditech, allscripts, athenahealth

_SYSTEMS = {
    epic.SYSTEM_KEY: epic,
    cerner.SYSTEM_KEY: cerner,
    meditech.SYSTEM_KEY: meditech,
    allscripts.SYSTEM_KEY: allscripts,
    athenahealth.SYSTEM_KEY: athenahealth,
}


class SourceSystemRuleSets:
    """Pre-configured rule sets for specific source systems."""

    @staticmethod
    def epic() -> RuleSet:
        return epic.ruleset()

    @staticmethod
    def cerner() -> RuleSet:
        return cerner.ruleset()

    @staticmethod
    def meditech() -> RuleSet:
        return meditech.ruleset()

    @staticmethod
    def allscripts() -> RuleSet:
        return allscripts.ruleset()

    @staticmethod
    def athenahealth() -> RuleSet:
        return athenahealth.ruleset()

    @staticmethod
    def get(system: str) -> RuleSet:
        key = system.strip().lower()
        if key not in _SYSTEMS:
            supported = ", ".join(sorted(_SYSTEMS.keys()))
            raise ValueError(f"Unsupported system '{system}'. Supported: {supported}")
        return _SYSTEMS[key].ruleset()

    @staticmethod
    def supported_systems() -> List[str]:
        return sorted(_SYSTEMS.keys())


def validate_source_system(data: pd.DataFrame, system: str):
    """
    Convenience function to validate a DataFrame against a system rule set.
    """
    ruleset = SourceSystemRuleSets.get(system)
    return ruleset.execute_all(data)


__all__ = ["SourceSystemRuleSets", "validate_source_system"]
