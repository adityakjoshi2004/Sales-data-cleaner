import csv
import json
import re

def clean_price(price_str):
    if not price_str or price_str.strip() == '':
        return None
    
    cleaned = price_str.replace('$', '').replace('"', '').replace(',', '').replace("'", '').strip()
    cleaned = re.sub(r'\[.*?\]', '', cleaned)
    
    try:
        return float(cleaned)
    except ValueError:
        return None

def clean_sales_data(input_file, output_file, usd_to_inr=83):
    clean_data = []
    seen_records = set()
    
    print(f"📂 Reading file: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            actual_gross_usd = clean_price(row.get('Actual\xa0gross', '') or row.get('Actual gross', ''))
            
            if actual_gross_usd is None:
                continue
            
            actual_gross_inr = actual_gross_usd * usd_to_inr
            adjusted_gross_usd = clean_price(row.get('Adjusted\xa0gross (in 2022 dollars)', '') or row.get('Adjusted gross (in 2022 dollars)', ''))
            adjusted_gross_inr = adjusted_gross_usd * usd_to_inr if adjusted_gross_usd else None
            average_gross_usd = clean_price(row.get('Average gross', ''))
            average_gross_inr = average_gross_usd * usd_to_inr if average_gross_usd else None
            
            artist = row.get('Artist', '').strip()
            tour_title = row.get('Tour title', '').strip()
            dedup_key = (artist, tour_title, actual_gross_usd)
            
            if dedup_key in seen_records:
                continue
            
            seen_records.add(dedup_key)
            
            clean_record = {
                'Rank': row.get('Rank', '').strip(),
                'Peak': row.get('Peak', '').strip(),
                'All Time Peak': row.get('All Time Peak', '').strip(),
                'Actual gross (USD)': actual_gross_usd,
                'Actual gross (INR)': round(actual_gross_inr, 2),
                'Adjusted gross USD (in 2022 dollars)': adjusted_gross_usd,
                'Adjusted gross INR (in 2022 dollars)': round(adjusted_gross_inr, 2) if adjusted_gross_inr else None,
                'Artist': artist,
                'Tour title': tour_title,
                'Year(s)': row.get('Year(s)', '').strip(),
                'Shows': row.get('Shows', '').strip(),
                'Average gross (USD)': average_gross_usd,
                'Average gross (INR)': round(average_gross_inr, 2) if average_gross_inr else None,
                'Ref.': row.get('Ref.', '').strip()
            }
            
            clean_data.append(clean_record)
    
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(clean_data, json_file, indent=2, ensure_ascii=False)
    
    print(f"✅ Data cleaned successfully!")
    print(f"📊 Total records processed: {len(clean_data)}")
    print(f"💾 Clean data saved to: {output_file}")
    
    return clean_data


input_file = "Messy_sales.csv"
output_file = "cleaned_sales.json"
usd_to_inr_rate = 83

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Sales Data Cleaner")
    print("="*60)
    print(f"📁 Input file: {input_file}")
    print(f"📁 Output file: {output_file}")
    print(f"💱 USD to INR rate: {usd_to_inr_rate}")
    print("="*60 + "\n")
    
    cleaned_data = clean_sales_data(input_file, output_file, usd_to_inr_rate)
    
    if cleaned_data:
        print("\n📋 Sample of cleaned data (first 3 records):")
        for i, record in enumerate(cleaned_data[:3], 1):
            print(f"\nRecord {i}:")
            print(f"  Artist: {record['Artist']}")
            print(f"  Tour: {record['Tour title']}")
            print(f"  Actual Gross (USD): ${record['Actual gross (USD)']:,.2f}")
            print(f"  Actual Gross (INR): ₹{record['Actual gross (INR)']:,.2f}")
    
    print("\n" + "="*60)
    print("✅ Process completed successfully!")
    print("="*60 + "\n")