# CV Data Transformer

This module transforms raw CV (marketing growth) data from CSV files to a standardized format. It handles the conversion from wide format (with days as columns) to long format with proper date handling and column standardization.

## Features

- Automatically processes all CSV files in the `gh_data` folder
- Transposes data from wide to long format
- Standardizes column names (lowercase, underscores, no special characters)
- Converts date formats (e.g., "June 1" to "2025-06-01")
- Handles different months with varying numbers of days
- Adds additional columns for future use

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from cv_transformer import CVTransformer

# Initialize transformer
transformer = CVTransformer()

# Transform all files and save to CSV
df = transformer.save_transformed_data("output.csv")
```

### Advanced Usage

```python
from cv_transformer import CVTransformer

# Initialize with custom data folder
transformer = CVTransformer(data_folder="my_data_folder")

# Transform a single file
df = transformer.transform_csv("path/to/file.csv")

# Transform all files without saving
df = transformer.transform_all_files()

# Get list of CSV files
csv_files = transformer.get_csv_files()
```

### Command Line Usage

Run the module directly to process all files:

```bash
python cv_transformer.py
```

## Input Format

The module expects CSV files with the following structure:
- First column: Metric names (e.g., "New Installs", "Sign up", etc.)
- Subsequent columns: Daily data for each day of the month
- Column headers: Date format like "June 1", "June 2", etc.

## Output Format

The transformed data includes:
- `report_day`: Standardized date format (YYYY-MM-DD)
- All original metrics as columns with cleaned names
- Additional placeholder columns for future use

## File Naming Convention

The module extracts month and year from filenames like:
`"Ghana - Marketing_Growth 360 Report - 2025 - June 2025 Overview.csv"`

## Error Handling

- Gracefully handles missing files
- Continues processing if one file fails
- Provides detailed error messages
- Validates input data structure

## Example

Input CSV structure:
```
7/3/2025,June 1,June 2,June 3,...
New Installs,2818,3287,4040,...
Sign up,2148,2691,3365,...
```

Output structure:
```
report_day,new_installs,sign_up,...
2025-06-01,2818,2148,...
2025-06-02,3287,2691,...
2025-06-03,4040,3365,...
``` 