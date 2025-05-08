# 🩺 NPI Healthcare Provider Data Cleaning and Normalization

This project demonstrates how to clean, extract, and normalize a large healthcare dataset (10GB+) of U.S. healthcare providers using Python.

## 📌 Objectives
- Extract key fields: contact info, professional info, taxonomy codes.
- Normalize address records (BP vs BM) and create one or two rows per provider.
- Clean missing name fields by falling back to Authorized Official information.
- Consolidate up to 15 taxonomy codes per provider with no internal gaps.
- Output a clean CSV with human-readable headers and structured rows.

## 🛠️ Tools Used
- Python (Pandas, optionally Dask for large file support)
- Jupyter for analysis and iteration
- CSV for output delivery

## 📂 Folder Structure
- `scripts/`: Contains the main cleaning script.
- `sample_data/`: Includes a 200-record sample file for demonstration.
- `output/`: Sample cleaned output for review.
- `summary/`: Summary statistics, including taxonomy code counts.

## 💡 Key Features
- Intelligent handling of missing or duplicate data
- Scalable design for 10GB+ files using chunked reading or Dask
- Clean and deduplicated output, ready for analytics or database insertion

## 🔄 To Run:
```bash
python scripts/clean_npi_dataset.py
```

## 👤 Author
Mariel Andrianavalondrahona — Data Analyst specializing in healthcare and large dataset processing
