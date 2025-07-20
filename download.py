import cdsapi
import time
import os
from datetime import datetime # <-- 1. Import the 'datetime' module

client = cdsapi.Client()

# --- NEW: Create a unique directory for this specific run ---
base_output_dir = 'Downloads'
# Get current time for the folder name, e.g., 'run_2025-07-20_10-55-00'
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
run_dir = os.path.join(base_output_dir, f'run_{timestamp}')

# Create the unique directory
os.makedirs(run_dir, exist_ok=True)
print(f"--- Created new download directory: {run_dir} ---")


# Define the bounding box for Saudi Arabia
saudi_arabia_area = [32.5, 34.5, 16, 56]

# Define the range of years you want
years_to_download = range(2004, 2006)

for year in years_to_download:
    print(f"--- Requesting data for year: {year} ---")
    try:
        # --- MODIFIED: Construct the full path inside the unique run directory ---
        output_path = os.path.join(run_dir, f'saudi_wind_speed_{year}.zip')

        client.retrieve(
            'sis-agrometeorological-indicators',
            {
                'variable': '10m_wind_speed',
                'statistic': '24_hour_mean',
                'year': str(year),
                'month': [
                    '01', '02', '03', '04', '05', '06',
                    '07', '08', '09', '10', '11', '12'
                ],
                'day': [
                    '01', '02', '03', '04', '05', '06',
                    '07', '08', '09', '10', '11', '12',
                    '13', '14', '15', '16', '17', '18',
                    '19', '20', '21', '22', '23', '24',
                    '25', '26', '27', '28', '29', '30', '31'
                ],
                'version': '2_0',
                'format': 'netcdf',
                'area': saudi_arabia_area,
            },
            # Use the new path variable here
            output_path
        )
        print(f"--- Successfully downloaded data for {year} to {run_dir} ---")

    except Exception as e:
        print(f"!!! Failed to download data for {year}. Error: {e} !!!")

    time.sleep(1)

print(">>> All downloads finished. <<<")
