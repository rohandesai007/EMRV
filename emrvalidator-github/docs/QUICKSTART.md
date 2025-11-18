# EMRValidator - Quick Start Guide

## Installation

### Option 1: Direct Installation
```bash
# Navigate to the emr_validator directory
cd emr_validator

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Option 2: Manual Setup
```bash
# Just install dependencies
pip install pandas numpy openpyxl xlrd

# Add emr_validator to your PYTHONPATH or copy to your project
```

## 5-Minute Tutorial

### 1. Basic Validation

```python
from emr_validator import DataValidator
import pandas as pd

# Load your data
df = pd.read_csv('your_data.csv')

# Create validator
validator = DataValidator("My First Validation")
validator.load_data(df)

# Add validations
validator.expect_column_exists('patient_id')
validator.expect_column_not_null('patient_id', threshold=0.99)

# Check results
if validator.is_valid():
    print("✓ Data is valid!")
else:
    print("Issues found:")
    for fail in validator.get_failed_validations():
        print(f"  - {fail['message']}")
```

### 2. Healthcare-Specific Validation

```python
# Validate MRN format
validator.expect_mrn_format('mrn', threshold=0.99)

# Validate ICD codes
validator.expect_icd_format('diagnosis_code', version=10)

# Validate age range
validator.expect_column_values_between('age', 0, 120)
```

### 3. Generate Reports

```python
from emr_validator import HTMLReporter

results = validator.get_results()
html_reporter = HTMLReporter(results)
html_reporter.generate('my_report.html')
```

### 4. Data Profiling

```python
from emr_validator import DataProfiler

profiler = DataProfiler(df, "My Dataset")
profile = profiler.generate_profile()

# Print summary
profiler.print_summary()

# Get quality score
quality_score = profile['quality_summary']['quality_score']
print(f"Quality Score: {quality_score}/100")
```

## Running the Examples

```bash
# Run all examples
python -m emr_validator.examples

# Or run directly
cd emr_validator
python examples.py
```

This will generate sample reports in `/mnt/user-data/outputs/`:
- `validation_report.html` - Beautiful HTML report
- `validation_report.json` - JSON export
- `validation_results.csv` - CSV results

## Common Use Cases

### Use Case 1: Patient Demographics Validation
```python
validator = DataValidator("Patient Demographics Check")
validator.load_data(patient_df)

(validator
    .expect_column_exists('mrn')
    .expect_column_exists('patient_id')
    .expect_column_not_null('mrn', threshold=1.0)
    .expect_column_values_unique('patient_id')
    .expect_column_values_in_set('gender', {'M', 'F', 'Other'})
    .expect_column_values_between('age', 0, 120)
    .expect_mrn_format('mrn')
)

# Generate report
results = validator.get_results()
HTMLReporter(results).generate('demographics_report.html')
```

### Use Case 2: Financial Data Validation
```python
validator = DataValidator("Financial Data Quality")
validator.load_data(billing_df)

(validator
    .expect_column_not_null('charge_amount', threshold=1.0)
    .expect_column_values_between('charge_amount', 0, 1000000)
    .expect_column_not_null('payment_amount', threshold=1.0)
)

# Custom validation: charges >= payments
def validate_charges(df, **kwargs):
    valid = (df['charge_amount'] >= df['payment_amount']).sum() / len(df)
    passed = valid > 0.98
    return passed, f"Valid charge/payment: {valid*100:.1f}%", {}

validator.expect_custom("charge_payment_logic", validate_charges)
```

### Use Case 3: Diagnosis Code Validation
```python
validator = DataValidator("Diagnosis Code Check")
validator.load_data(claims_df)

(validator
    .expect_column_exists('icd10_code')
    .expect_column_not_null('icd10_code', threshold=0.95)
    .expect_icd_format('icd10_code', version=10, threshold=0.98)
)
```

## Best Practices

1. **Always profile first** - Use DataProfiler to understand your data
2. **Set realistic thresholds** - Use 0.95-0.99 instead of 1.0
3. **Use method chaining** - Makes code cleaner and more readable
4. **Generate HTML reports** - Great for stakeholders and documentation
5. **Mark critical validations** - Use `critical=True` for must-pass checks

## Troubleshooting

### Import Error
```python
# Make sure you're in the right directory
import sys
sys.path.append('/path/to/emr_validator')
from emr_validator import DataValidator
```

### Memory Issues with Large Files
```python
# Read in chunks for very large files
chunk_size = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    validator = DataValidator("Chunk Validation")
    validator.load_data(chunk)
    # ... run validations
```

## Next Steps

1. Read the full [README.md](README.md) for comprehensive documentation
2. Explore [examples.py](examples.py) for more use cases
3. Create custom validation rules for your specific needs
4. Build reusable rule sets for common patterns

## Support

For questions or issues:
- Check the README.md for detailed documentation
- Review examples.py for code samples
- Examine the source code - it's well documented!

---

**Happy Validating! 🎉**
