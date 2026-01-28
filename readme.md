Sales Data Cleaner – ETL Pipeline
Project Goal

A Python-based ETL script that cleans messy CSV sales data by removing special characters, deduplicating records, converting USD prices to INR, and exporting structured JSON suitable for analytics and machine learning pipelines.

Setup Instructions
Prerequisites

Python 3.x

No external libraries required (uses only the Python standard library)

Steps to Run
# Place the messy CSV file in the project directory
# or provide an absolute path in the script


# Edit configuration in the script:
# input_file = "YOUR_FILE_NAME.csv"
# output_file = "clean_sales.json"
# usd_to_inr_rate = 83


python clean_sales_simple.py

After execution, the cleaned data will be saved as a JSON file in the specified output location.

The Logic (How I Thought)
Why This Approach Was Chosen

Use of Python Standard Library Only
The script uses only built-in modules such as csv, json, and re. This avoids dependency-related issues, improves portability, and ensures the script can run on any system with Python installed.

Regex-Based Data Cleaning
Regular expressions were used to remove embedded annotations such as reference markers ([1], [a], etc.) that appear in scraped or exported datasets. Simple string replacement was preferred for common symbols like dollar signs and commas due to better readability and performance.

Efficient Deduplication Using Sets
Deduplication is handled using a Python set, allowing constant-time lookups. Records are deduplicated based on business-relevant fields rather than relying solely on IDs, which are not always reliable in real-world datasets.

Handling Non-Breaking Spaces in Headers
The CSV file contained non-breaking spaces (\xa0) in column headers, a common issue in files exported from web sources or spreadsheet tools. The script explicitly checks for both standard and non-breaking space variants to ensure compatibility.

Centralized Configuration
All configurable values such as file paths and conversion rates are grouped together, allowing easy modification without changing core logic. This improves maintainability and readability.

Hardest Bug Faced and How It Was Fixed

Problem:
The script processed zero records even though the CSV contained valid data.

Root Cause:
Column headers included non-breaking spaces (\xa0) instead of regular spaces. This caused key lookups like "Actual gross" to fail silently.

Debugging Process:

Printed csv_reader.fieldnames to inspect headers

Identified invisible non-breaking spaces in column names

Confirmed mismatch between expected and actual header strings

Fix Implemented:
The script now checks for both versions of the column name:

actual_gross_usd = clean_price(
    row.get("Actual\xa0gross", "") or row.get("Actual gross", "")
)

Lesson Learned:
Always inspect CSV headers programmatically. Non-breaking spaces are common in real-world datasets and can cause subtle bugs.

Output Proof
Cleaned JSON Output

<img width="1742" height="447" alt="image" src="https://github.com/user-attachments/assets/44d83c3f-8aea-4483-95e2-916e5ae22008" />
<img width="863" height="763" alt="image" src="https://github.com/user-attachments/assets/ef49f672-eefa-470b-a5b0-e6ce4dfdbb4f" />


The script successfully processed 20 records and generated structured JSON data.


Verification Summary

Currency symbols and commas removed

Numeric fields converted to floats

USD values converted to INR using a fixed rate

Output structured in JSON format

Duplicate records removed

Future Improvements

If given additional time, the following enhancements would be implemented:

Data Validation

Schema checks for numeric and date fields

Detection of invalid or outlier values

Validation report generation

Multi-Currency Support

Conversion to multiple currencies

Optional live exchange rate integration

Configurable currency targets

Data Quality Reporting

Summary of processed vs skipped records

Duplicate detection statistics

Distribution analysis of numeric fields

Batch Processing

Ability to process multiple CSV files

Consolidated output generation

Progress tracking for large datasets

Database Export

Optional export to SQLite or PostgreSQL

Structured relational schema

Incremental update support

Logging and Error Handling

Structured logging using Python’s logging module

Error trace files for debugging

Graceful handling of malformed rows

Configuration Files

Support for config.json or config.yaml

Environment-based profiles (development, production)

Performance Optimization

Streaming for very large files

Optional multiprocessing

Profiling and benchmarking

Summary

This project demonstrates a practical ETL workflow with real-world data challenges:

Clean and dependency-free implementation

Robust handling of messy CSV exports

Efficient deduplication and transformation logic

Output suitable for analytics and machine learning use cases

All records were processed successfully with consistent and reliable results.
