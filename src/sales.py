import pandas as pd
from datetime import datetime

def audit_material_price_variance(input_file, output_file='price_variance_report.xlsx'):
    """
    Audits material sales to identify when same customer bought same material 
    on same date at different basic rates.
    
    Parameters:
    input_file: Path to input Excel/CSV file
    output_file: Path to output Excel file (default: price_variance_report.xlsx)
    """
    
    # Read the input file
    try:
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
        else:
            df = pd.read_excel(input_file)
        
        print(f"✓ File loaded successfully. Total records: {len(df)}")
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return
    
    # Normalize column names to uppercase for consistency
    df.columns = df.columns.str.upper()
    
    # Required columns (uppercase)
    required_cols = [
        'MATERIAL DESCRIPTION',
        'SO CREATED ON',
        'MATERIAL CODE',
        'SOLD TO PARTY NAME',
        'BASIC RATE'
    ]
    
    # Check if required columns exist
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"✗ Missing required columns: {missing_cols}")
        return
    
    # Convert 'SO CREATED ON' to datetime
    df['SO CREATED ON'] = pd.to_datetime(df['SO CREATED ON'], errors='coerce')
    
    # Remove rows with missing critical data
    df_clean = df.dropna(subset=[
        'MATERIAL CODE',
        'SO CREATED ON',
        'SOLD TO PARTY NAME',
        'BASIC RATE'
    ])
    
    print(f"✓ Records after cleaning: {len(df_clean)}")
    
    # Group by customer, material code, and date
    grouped = df_clean.groupby(['SOLD TO PARTY NAME', 'MATERIAL CODE', 'SO CREATED ON'])
    
    variance_groups = []
    
    for (party_name, material_code, doc_date), group in grouped:
        unique_rates = group['BASIC RATE'].unique()
        
        if len(unique_rates) > 1:
            max_rate = group['BASIC RATE'].max()
            min_rate = group['BASIC RATE'].min()
            
            row_label = f"{party_name} | {material_code} | {doc_date.strftime('%Y-%m-%d')}"
            
            variance_groups.append({
                'Customer_Material_Date': row_label,
                'Max Rate': max_rate,
                'Min Rate': min_rate,
                'Diff': round(max_rate - min_rate, 2)
            })
    
    if not variance_groups:
        print("\n✓ No price variances detected. All materials have consistent basic rates.")
        return
    
    # Create DataFrame from variance records
    variance_df = pd.DataFrame(variance_groups)
    
    # Sort by difference descending
    variance_df = variance_df.sort_values('Diff', ascending=False)
    
    # Save to Excel
    try:
        variance_df.to_excel(output_file, index=False, sheet_name='Price Variances')
        
        print(f"\n✓ Price variance report generated: {output_file}")
        print("\n" + "="*60)
        print("AUDIT SUMMARY")
        print("="*60)
        print(f"Total Variance Cases: {len(variance_df)}")
        print(f"Average Price Difference: {round(variance_df['Diff'].mean(), 2)}")
        print(f"Maximum Price Difference: {round(variance_df['Diff'].max(), 2)}")
        print(f"Minimum Price Difference: {round(variance_df['Diff'].min(), 2)}")
        print("="*60)
        
        # Show top 10 variances
        print("\nTop 10 Price Variances:")
        print(variance_df.head(10).to_string(index=False))
    
    except Exception as e:
        print(f"✗ Error writing output file: {e}")

# Example usage
if __name__ == "__main__":
    input_file = 'input.xlsx'  # replace with your actual file
    output_file = 'material_price_variance_audit_report.xlsx'
    
    print("="*60)
    print("MATERIAL PRICE VARIANCE AUDIT TOOL")
    print("="*60)
    print("Logic: SOLD TO PARTY NAME + MATERIAL CODE + SAME DATE")
    print("="*60)
    print()
    
    audit_material_price_variance(input_file, output_file)
    
    print("\nAudit complete!")
