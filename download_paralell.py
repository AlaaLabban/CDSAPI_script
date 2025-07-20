import cdsapi
import time
import os
from datetime import datetime
from multiprocessing import Pool


# --- IMPORTANT: This function must be defined at the top level ---
def download_year(year, output_dir):
    """
    This function contains the logic to download data for a single year.
    It will be run by each parallel process.
    """
    print(f"--- Starting request for year: {year} ---")
    try:
        # Each process needs its own client instance
        client = cdsapi.Client()

        # Define the bounding box for Saudi Arabia
        saudi_arabia_area = [32.5, 34.5, 16, 56]

        # Construct the full path for the output file inside the unique run directory
        output_path = os.path.join(output_dir, f'saudi_wind_speed_{year}.zip')

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
                'format': 'zip',
                'area': saudi_arabia_area,
            },
            output_path
        )
        # A small delay to be considerate to the API server upon completion
        time.sleep(1)
        return f"--- Successfully downloaded data for {year} to {output_dir} ---"

    except Exception as e:
        return f"!!! Failed to download data for {year}. Error: {e} !!!"


# --- Main part of the script ---
if __name__ == '__main__':
    # --- Create a unique directory for this specific run ---
    base_output_dir = 'Downloads_paralell'
    # Get current time for the folder name, e.g., 'run_2025-07-20_10-30-00'
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    run_dir = os.path.join(base_output_dir, f'run_{timestamp}')

    # Create the unique directory
    os.makedirs(run_dir, exist_ok=True)
    print(f"--- Created new download directory: {run_dir} ---")

    # Define the range of years you want
    years_to_download = list(range(1979, 1983))

    # Prepare arguments for starmap: a list of (year, output_directory) tuples
    tasks = [(year, run_dir) for year in years_to_download]

    # Create a pool of 4 worker processes
    with Pool(processes=4) as pool:
        # Use starmap to pass multiple arguments to the download function
        results = pool.starmap(download_year, tasks)

        # Print the results/status for each completed download
        for result in results:
            print(result)

    print(">>> All parallel downloads finished. <<<")
