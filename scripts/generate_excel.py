import json
import pandas as pd
import os

def generate_excel():
    json_path = 'data/schools.json'
    output_path = 'data/Hyderabad_CBSE_Schools.xlsx'

    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    with open(json_path, 'r') as f:
        data = json.load(f)

    # Extract Hyderabad schools
    # Data structure is State -> District -> List of Schools
    schools_list = []

    try:
        hyderabad_schools = data.get('Telangana', {}).get('Hyderabad', [])

        for school in hyderabad_schools:
            schools_list.append({
                'School Name': school.get('name', ''),
                'Email ID': school.get('email', ''),
                'Address': school.get('address', ''),
                'Contact Number': school.get('phone', '')
            })

    except Exception as e:
        print(f"Error processing data: {e}")
        return

    if not schools_list:
        print("No schools found for Hyderabad.")
        df = pd.DataFrame(columns=['School Name', 'Email ID', 'Address', 'Contact Number'])
    else:
        df = pd.DataFrame(schools_list)

    # Reorder columns just in case
    df = df[['School Name', 'Email ID', 'Address', 'Contact Number']]

    print(f"Found {len(df)} schools in Hyderabad.")

    try:
        df.to_excel(output_path, index=False)
        print(f"Excel file created at: {output_path}")
    except Exception as e:
        print(f"Error saving Excel file: {e}")

if __name__ == "__main__":
    generate_excel()
