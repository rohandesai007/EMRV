"""
Core DataValidator class for EMR data validation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Callable, Any, Protocol
from datetime import datetime
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ValidationFunction(Protocol):
    def __call__(self, data: pd.DataFrame, **kwargs) -> tuple[bool, str, Dict[str, Any]]:
        pass

class DataValidator:
    """
    Main validation engine for healthcare data.
    
    Simplified API compared to Great Expectations with better performance
    and healthcare-specific features.
    """
    
    def __init__(self, name: str = "EMR Validation"):
        """
        Initialize validator
        
        Args:
            name: Name for this validation context
        """
        self.name = name
        self.data: Optional[pd.DataFrame] = None
        self.validation_results = pd.DataFrame(columns=[
            "rule", "column", "critical", "passed", "message", "details"
        ])
        self.metadata = {
            "created_at": datetime.now().isoformat(),
            "name": name,
            "total_validations": 0,
            "passed": 0,
            "failed": 0,
            "warnings": 0
        }
        
    def load_data(
        self,
        data: Union[pd.DataFrame, str, Path],
        column_aliases: Optional[Dict[str, Union[str, List[str]]]] = None,
        source_system: Optional[str] = None,
        warn_large_file_mb: int = 250,
        csv_chunksize: int = 100000,
        chunk_on_large: bool = True,
    ) -> 'DataValidator':
        """
        Load data for validation
        
        Args:
            data: DataFrame or path to CSV/Excel file
            column_aliases: Map of canonical column name to aliases
            source_system: Source system name to apply default aliases
            warn_large_file_mb: Warn when file exceeds this size (MB)
            csv_chunksize: CSV chunk size used when chunk_on_large=True
            chunk_on_large: Use chunked CSV reads when file exceeds warn_large_file_mb
            
        Returns:
            Self for method chaining
        """
        if isinstance(data, pd.DataFrame):
            self.data = data.copy()
        elif isinstance(data, (str, Path)):
            file_path = Path(data)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            if not file_path.is_file():
                raise ValueError(f"Path is not a file: {file_path}")

            size_mb = file_path.stat().st_size / (1024 * 1024)
            if size_mb >= warn_large_file_mb:
                logger.warning(
                    "Large file detected (%.1f MB). Consider chunked reads or sampling.",
                    size_mb,
                )

            suffix = file_path.suffix.lower()
            try:
                if suffix == '.csv':
                    if chunk_on_large and size_mb >= warn_large_file_mb:
                        chunks = pd.read_csv(file_path, chunksize=csv_chunksize)
                        self.data = pd.concat(chunks, ignore_index=True)
                    else:
                        self.data = pd.read_csv(file_path)
                elif suffix in ['.xlsx', '.xls']:
                    self.data = pd.read_excel(file_path)
                else:
                    raise ValueError(f"Unsupported file format: {file_path.suffix}")
            except pd.errors.EmptyDataError as exc:
                raise ValueError(f"File is empty: {file_path}") from exc
            except pd.errors.ParserError as exc:
                raise ValueError(f"Failed to parse file: {file_path}") from exc
            except PermissionError as exc:
                raise PermissionError(f"Permission denied: {file_path}") from exc
            except ImportError as exc:
                raise ImportError("Excel support requires 'emrvalidator[excel]'") from exc
        else:
            raise TypeError("Data must be DataFrame or file path")
            
        merged_aliases: Dict[str, Union[str, List[str]]] = {}
        if source_system:
            from .source_systems import get_system_aliases

            merged_aliases.update(get_system_aliases(source_system))
        if column_aliases:
            merged_aliases.update(column_aliases)
        if merged_aliases:
            self._apply_column_aliases(merged_aliases)

        self.metadata["total_rows"] = len(self.data)
        self.metadata["total_columns"] = len(self.data.columns)
        if self.metadata["total_rows"] == 0:
            logger.warning("Loaded data has zero rows; validations may fail.")
        return self

    def _apply_column_aliases(self, column_aliases: Dict[str, Union[str, List[str]]]) -> None:
        if self.data is None:
            return

        renamed = {}
        for canonical, aliases in column_aliases.items():
            if canonical in self.data.columns:
                continue

            alias_list = [aliases] if isinstance(aliases, str) else list(aliases)
            found = [col for col in alias_list if col in self.data.columns]
            if not found:
                continue

            chosen = found[0]
            if len(found) > 1:
                logger.warning(
                    "Multiple aliases found for '%s'; using '%s': %s",
                    canonical,
                    chosen,
                    ", ".join(found),
                )
            renamed[chosen] = canonical

        if renamed:
            self.data = self.data.rename(columns=renamed)

    def _ensure_data_loaded(self) -> None:
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() before validations.")

    def expect_column_exists(self, column: str, critical: bool = True) -> 'DataValidator':
        """
        Check if column exists in dataset.

        Args:
            column: The name of the column to check.
            critical: Whether this validation is critical.

        Returns:
            Self for method chaining.
        """
        self._ensure_data_loaded()
        result = {
            "rule": "column_exists",
            "column": column,
            "critical": critical,
            "passed": column in self.data.columns,
            "message": f"Column '{column}' exists" if column in self.data.columns else f"Column '{column}' missing"
        }
        self._record_result(result)
        return self

    def expect_column_not_null(self, column: str, threshold: float = 1.0, critical: bool = True) -> 'DataValidator':
        """
        Check for null values in column using vectorized pandas operations.
        
        Args:
            column: Column name
            threshold: Minimum non-null percentage (0.0 to 1.0)
            critical: Whether this is a critical validation
        """
        self._ensure_data_loaded()
        if len(self.data) == 0:
            return self._record_failure("column_not_null", column, critical, "No rows to validate")
        if column not in self.data.columns:
            return self._record_failure("column_not_null", column, critical, f"Column '{column}' does not exist")

        series = self.data[column]
        non_null_frac = float(series.notna().mean())
        passed = non_null_frac >= threshold
        pct = round(non_null_frac * 100, 2)

        result = {
            "rule": "column_not_null",
            "column": column,
            "critical": critical,
            "passed": passed,
            "non_null_percentage": pct,
            "threshold": threshold * 100,
            "null_count": int(series.isna().sum()),
            "message": f"Non-null percentage for '{column}': {pct}% (threshold {threshold*100}%)"
        }
        self._record_result(result)
        return self

    def expect_column_values_in_set(self, column: str, value_set: set, 
                                   threshold: float = 1.0, critical: bool = True) -> 'DataValidator':
        """
        Check if column values are in allowed set using vectorized membership checks.
        
        Args:
            column: Column name
            value_set: Set of allowed values
            threshold: Minimum percentage of rows that must match (0.0 to 1.0)
            critical: Whether this is a critical validation
        """
        self._ensure_data_loaded()
        if len(self.data) == 0:
            return self._record_failure("values_in_set", column, critical, "No rows to validate")
        if column not in self.data.columns:
            return self._record_failure("values_in_set", column, critical, f"Column '{column}' does not exist")

        series = self.data[column]
        mask = series.isin(value_set)
        valid_frac = float(mask.mean())
        passed = valid_frac >= threshold
        pct = round(valid_frac * 100, 2)

        invalid_values = series.loc[~mask].dropna().unique()

        result = {
            "rule": "values_in_set",
            "column": column,
            "critical": critical,
            "passed": passed,
            "valid_percentage": pct,
            "threshold": threshold * 100,
            "invalid_count": int((~mask).sum()),
            "invalid_values": list(invalid_values[:10]),
            "message": f"Values in set for '{column}': {pct}% (threshold {threshold*100}%)"
        }
        self._record_result(result)
        return self

    def _record_failure(self, rule: str, column: str, critical: bool, message: str) -> 'DataValidator':
        """
        Helper method to record a failed validation.
        """
        result = {
            "rule": rule,
            "column": column,
            "critical": critical,
            "passed": False,
            "message": message
        }
        self._record_result(result)
        return self

    def _record_result(self, result: Dict[str, Any]) -> None:
        """
        Record validation result and update metadata.
        """
        self.validation_results = pd.concat(
            [self.validation_results, pd.DataFrame([result])],
            ignore_index=True
        )
        self.metadata["total_validations"] += 1

        if result["passed"]:
            self.metadata["passed"] += 1
            logger.info(f"Validation passed: {result['message']}")
        elif result.get("critical", True):
            self.metadata["failed"] += 1
            logger.error(f"Validation failed: {result['message']}")
        else:
            self.metadata["warnings"] += 1
            logger.warning(f"Validation warning: {result['message']}")



            