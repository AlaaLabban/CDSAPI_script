import os
import glob
import zipfile
import xarray as xr
import re  # Import the regular expressions module

# --- Define the base input and output directories ---
base_input_dir = 'Downloads'
output_dir = 'Merged'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# --- Part 1: Find the latest run directory ---
print(f"--- Searching for latest run in '{base_input_dir}'... ---")
try:
    # Get all subdirectories in the base input directory
    all_runs = [d for d in os.listdir(base_input_dir) if os.path.isdir(os.path.join(base_input_dir, d))]
    if not all_runs:
        raise FileNotFoundError(f"No run directories found in '{base_input_dir}'")

    # The latest directory will be the last one when sorted alphabetically
    latest_run_folder = sorted(all_runs)[-1]
    # This is the directory we will work with
    input_dir = os.path.join(base_input_dir, latest_run_folder)
    print(f"Found latest run directory: {input_dir}")

except FileNotFoundError as e:
    print(e)
    exit()  # Exit the script if no directories are found

# --- Part 2: Unzip all the downloaded files ---
print(f"\n--- Unzipping files from '{input_dir}'... ---")
zip_files = glob.glob(os.path.join(input_dir, '*.zip'))

if not zip_files:
    print(f"No .zip files found in '{input_dir}'.")
else:
    for zip_path in zip_files:
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Extract files into the same directory
                zip_ref.extractall(input_dir)
            print(f"Extracted: {os.path.basename(zip_path)}")
        except Exception as e:
            print(f"Error extracting {zip_path}: {e}")

# --- Part 3: Merge the extracted NetCDF files ---
print(f"\n--- Merging all NetCDF files from '{input_dir}'... ---")
netcdf_files = sorted(glob.glob(os.path.join(input_dir, '*.nc')))

if not netcdf_files:
    print(f"No NetCDF files found to merge in '{input_dir}'. Make sure the zip files were extracted correctly.")
else:
    try:
        # --- NEW: Dynamically determine the year range ---
        years = []
        for f in netcdf_files:
            # Use regex to find a 4-digit number (the year) in the filename
            match = re.search(r'\d{4}', os.path.basename(f))
            if match:
                years.append(int(match.group(0)))

        start_year = min(years)
        end_year = max(years)

        # Using the more robust manual merging method
        list_of_datasets = []
        print("Opening files one by one...")
        for f in netcdf_files:
            ds = xr.open_dataset(f)
            list_of_datasets.append(ds)

        print("Combining datasets...")
        merged_dataset = xr.concat(list_of_datasets, dim='time')

        # --- MODIFIED: Use the dynamic year range in the filename ---
        output_filename = f'saudi_wind_speed_{start_year}-{end_year}_MERGED.nc'
        output_path = os.path.join(output_dir, output_filename)

        print(f"Saving final merged file to '{output_dir}' directory...")
        merged_dataset.to_netcdf(output_path)

        print(f"\n✅ Successfully merged {len(netcdf_files)} files into:")
        print(output_path)

    except Exception as e:
        print(f"An error occurred during merging: {e}")
