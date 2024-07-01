import pandas as pd
import json

def create_json_helper():

    cars = pd.read_csv('AmericanCarPricePredictor/data/cleaned_data.csv')

    manufacturers = cars['Manufacturer'].unique().tolist()
    categories = cars['Category'].unique().tolist()
    fuel_types = cars['Fuel type'].unique().tolist()
    gear_box_types = cars['Gear box type'].unique().tolist()
    drive_wheel_types = cars['Drive wheels'].unique().tolist()
    wheel_types = cars['Wheel'].unique().tolist()
    color_types = cars['Color'].unique().tolist()

    json_data = {
        "manufacturers": sorted(manufacturers),
        'categories': sorted(categories),
        'fuel_types': sorted(fuel_types),
        'gear_box_types': sorted(gear_box_types),
        'drive_wheel_types': sorted(drive_wheel_types),
        'wheel_types': sorted(wheel_types),
        'color_types': sorted(color_types)
    }

    for manufacturer in manufacturers:
        models = cars[cars['Manufacturer'] == manufacturer]['Model'].unique().tolist()
        json_data[f'{manufacturer}_models'] = sorted(models)

    with open('strings.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)