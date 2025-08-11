#!/usr/bin/env python3
"""
Script to check Excel file contents
"""
import pandas as pd
import sys

def check_excel_file(filename):
    try:
        # Read Excel file
        df = pd.read_excel(filename, sheet_name='Dataset Alergen')
        
        print(f"Excel file: {filename}")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst 5 rows:")
        print(df.head())
        
        # Check if first column is 'No' or 'id'
        first_col = df.columns[0]
        print(f"\nFirst column name: '{first_col}'")
        print(f"First column values: {df[first_col].head().tolist()}")
        
        # Check if there's an ID column
        if 'id' in df.columns:
            print("WARNING: 'id' column still exists!")
            print(f"ID values: {df['id'].head().tolist()}")
        else:
            print("✅ No 'id' column found - numbering working correctly")
            
    except Exception as e:
        print(f"Error reading Excel file: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_excel_file(sys.argv[1])
    else:
        # Check all test files
        import glob
        excel_files = glob.glob("test*.xlsx")
        for file in excel_files:
            print("=" * 50)
            check_excel_file(file)
            print("=" * 50)
