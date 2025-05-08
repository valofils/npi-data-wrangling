# clean_npi_dataset.py

import pandas as pd
import os

# Paths
input_file = "sample_data/NPI_Sample_200_Records.csv"
output_file = "output/cleaned_output_example.csv"
taxonomy_summary_file = "summary/taxonomy_counts.csv"

# Load data
df = pd.read_csv(input_file, dtype=str)

# Normalize address columns for comparison
def normalize_address(row):
    fields = [
        row.get('Provider First Line Business Practice Location Address', ''),
        row.get('Provider Second Line Business Practice Location Address', ''),
        row.get('Provider Business Practice Location City Name', ''),
        row.get('Provider Business Practice Location State Name', ''),
        row.get('Provider Business Practice Location Postal Code', ''),
    ]
    return ' '.join(str(f).strip().lower().replace(',', '').replace('.', '') for f in fields)

def normalize_mailing(row):
    fields = [
        row.get('Provider First Line Business Mailing Address', ''),
        row.get('Provider Second Line Business Mailing Address', ''),
        row.get('Provider Business Mailing Address City Name', ''),
        row.get('Provider Business Mailing Address State Name', ''),
        row.get('Provider Business Mailing Address Postal Code', ''),
    ]
    return ' '.join(str(f).strip().lower().replace(',', '').replace('.', '') for f in fields)

def get_name(row):
    if pd.notna(row.get('Provider First Name')) and pd.notna(row.get('Provider Last Name (Legal Name)')):
        return row.get('Provider First Name'), row.get('Provider Last Name (Legal Name)')
    return row.get('Authorized Official First Name'), row.get('Authorized Official Last Name')

def consolidate_taxonomy(row):
    codes = [row.get(f"Healthcare Provider Taxonomy Code_{i}", None) for i in range(1, 16)]
    return [code for code in codes if pd.notna(code)]

records = []

for _, row in df.iterrows():
    first_name, last_name = get_name(row)
    credential = row.get('Provider Credential Text', '')
    org_name = row.get('Provider Organization Name (Legal Business Name)', '')

    taxonomy_codes = consolidate_taxonomy(row)
    taxonomy_data = {f"Taxonomy Code_{i+1}": taxonomy_codes[i] if i < len(taxonomy_codes) else ''
                     for i in range(15)}

    bp_address = normalize_address(row)
    bm_address = normalize_mailing(row)

    common_data = {
        "NPI": row["NPI"],
        "First Name": first_name,
        "Last Name": last_name,
        "Credential": credential,
        "Organization Name": org_name,
        "Enumeration Date": row.get("Provider Enumeration Date", ""),
        "License Number": row.get("Provider License Number_1", ""),
        "License State": row.get("Provider License Number State Code_1", ""),
        "Phone Number": row.get("Provider Business Practice Location Telephone Number", "") or row.get("Provider Business Mailing Address Telephone Number", "")
    }
    common_data.update(taxonomy_data)

    if bp_address == bm_address:
        records.append({
            **common_data,
            "Street Address": row.get("Provider First Line Business Practice Location Address", ""),
            "City": row.get("Provider Business Practice Location City Name", ""),
            "State": row.get("Provider Business Practice Location State Name", ""),
            "Zip Code": row.get("Provider Business Practice Location Postal Code", ""),
            "Address Type": "BP"
        })
    else:
        # Add BP
        records.append({
            **common_data,
            "Street Address": row.get("Provider First Line Business Practice Location Address", ""),
            "City": row.get("Provider Business Practice Location City Name", ""),
            "State": row.get("Provider Business Practice Location State Name", ""),
            "Zip Code": row.get("Provider Business Practice Location Postal Code", ""),
            "Address Type": "BP"
        })
        # Add BM
        records.append({
            **common_data,
            "Street Address": row.get("Provider First Line Business Mailing Address", ""),
            "City": row.get("Provider Business Mailing Address City Name", ""),
            "State": row.get("Provider Business Mailing Address State Name", ""),
            "Zip Code": row.get("Provider Business Mailing Address Postal Code", ""),
            "Address Type": "BM"
        })

# Create cleaned DataFrame
cleaned_df = pd.DataFrame(records)

# Save output
os.makedirs("output", exist_ok=True)
os.makedirs("summary", exist_ok=True)
cleaned_df.to_csv(output_file, index=False)

# Create taxonomy summary
all_codes = cleaned_df[[f"Taxonomy Code_{i+1}" for i in range(15)]].values.flatten()
code_series = pd.Series(all_codes)
taxonomy_counts = code_series[code_series != ''].value_counts().reset_index()
taxonomy_counts.columns = ["Taxonomy Code", "Count"]
taxonomy_counts.to_csv(taxonomy_summary_file, index=False)

print("✅ Cleaning completed. Files saved in /output and /summary.")
