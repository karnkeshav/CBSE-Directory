import json
import os
import shutil

def create_structure():
    json_path = 'data/all_india_districts.json'
    base_path = 'data'

    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    with open(json_path, 'r') as f:
        data = json.load(f)

    states = data.get('states', [])

    for state_obj in states:
        state_name = state_obj.get('state')
        districts = state_obj.get('districts', [])

        # Clean state name for folder
        state_folder = os.path.join(base_path, state_name.strip())
        os.makedirs(state_folder, exist_ok=True)
        print(f"Created state folder: {state_folder}")

        for district in districts:
            district_name = district.strip()
            # Handle slashes in district names if any
            district_name = district_name.replace('/', '_')

            district_folder = os.path.join(state_folder, district_name)
            os.makedirs(district_folder, exist_ok=True)
            # print(f"Created district folder: {district_folder}")

if __name__ == "__main__":
    create_structure()
