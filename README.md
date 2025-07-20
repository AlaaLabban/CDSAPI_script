# Copernicus Climate Data Workflow

## 🚀 Overview

This project provides a complete workflow to download, process, and merge large climate datasets from the Copernicus Climate Data Store (CDS).

It is designed to handle multi-year data requests efficiently by breaking them into smaller yearly chunks, downloading them (sequentially or in parallel), and then combining them into a single, analysis-ready NetCDF file.

## ✨ Features

-   **Automated Downloading**: Fetches data for specified variables, years, and geographic areas.
-   **Dual Download Modes**:
    -   **Sequential**: Simple and reliable, downloads one year at a time.
    -   **Parallel**: Significantly faster, downloads multiple years simultaneously.
-   **Smart Organization**: Automatically saves each download session into a unique, timestamped folder to prevent data loss.
-   **Automated Processing**: Finds the latest downloaded data, unzips the yearly files, and merges them into a final dataset.
-   **Dynamic Filenaming**: The final merged file is automatically named with the correct start and end year (e.g., `..._2004-2006_MERGED.nc`).

---

## 🛠️ Prerequisites & Setup

Before you begin, you must configure your environment.

### 1. Copernicus CDS API Key

You must have a Copernicus account and an API key.

1.  Register for an account on the [CDS registration page](https://cds.climate.copernicus.eu/user/register).
2.  Log in and visit the [API how-to page](https://cds.climate.copernicus.eu/api-how-to) to find your **UID** and **API Key**.
3.  In your system's **home directory** (`/home/your_username/`), create a file named `.cdsapirc`.
4.  Add your credentials to the file in the following format:
    ```
    url: [https://cds.climate.copernicus.eu/api/v2](https://cds.climate.copernicus.eu/api/v2)
    key: YOUR_UID:YOUR_API_KEY
    ```

### 2. Python Libraries

Install the required Python packages using `pip`.

```bash
pip install cdsapi xarray netcdf4 dask
```

### 3. Accept Terms of Use

For any new dataset, you must visit its page on the CDS website and manually accept the "Terms of Use" before the API will allow you to download it.

---

## ⚙️ Workflow and Usage

The process involves two main steps: **Download** and **Merge**. Choose the workflow that best suits your needs.

### Method 1: Sequential Workflow (Simple)

This method is reliable and easy to follow. It downloads one year at a time.

* **Step 1: Download Data**
    Run the `download.py` script. It will create a new timestamped folder inside `Downloads/` and save the yearly `.zip` files there.
    ```bash
    python download.py
    ```

* **Step 2: Unzip and Merge Data**
    Once the download is complete, run the `unzip_merge.py` script. It automatically finds the latest folder in `Downloads/`, unzips the files, and saves a single combined file into the `Merged/` directory.
    ```bash
    python unzip_merge.py
    ```

### Method 2: Parallel Workflow (Fast)

This method is much faster for large date ranges as it downloads multiple years at once.

* **Step 1: Download Data in Parallel**
    Run the `download_paralell.py` script. It will create a new timestamped folder inside `Downloads_paralell/` and save the yearly `.zip` files there.
    ```bash
    python download_paralell.py
    ```

* **Step 2: Unzip and Merge Data**
    After the download finishes, run the `unzip_merge_paralell.py` script. It finds the latest folder in `Downloads_paralell/`, unzips the files, and saves a single combined file into the `Merged_paralell/` directory.
    ```bash
    python unzip_merge_paralell.py
    ```

### Step 3: Examine the Final File

Use the `examine.py` script to inspect the structure and contents of your final merged NetCDF file. **Remember to update the `filename` variable inside the script to point to your new file.**

```bash
python examine.py
```

---

## 📜 Script Descriptions

* **`download.py`**: Downloads data sequentially. Saves to `Downloads/run_[timestamp]`.
* **`download_paralell.py`**: Downloads data in parallel for maximum speed. Saves to `Downloads_paralell/run_[timestamp]`.
* **`unzip_merge.py`**: Processes data from the sequential download.
* **`unzip_merge_paralell.py`**: Processes data from the parallel download.
* **`examine.py`**: A utility script to print a summary of a NetCDF file.

## 🔧 Configuration

To download different data, edit the download scripts (`download.py` or `download_paralell.py`):

* **Years**: Modify the `years_to_download` variable (e.g., `range(2000, 2010)` for years 2000-2009).
* **Location**: Modify the `saudi_arabia_area` list. The format is `[North_Latitude, West_Longitude, South_Latitude, East_Longitude]`.
* **Variable**: Change the `'variable'` and `'statistic'` values inside the `client.retrieve` call.

## 🩺 Troubleshooting

If your download fails, check these common issues:

1.  **Check the error message**: It will often tell you exactly what is wrong.
2.  **API Key**: Ensure the `.cdsapirc` file is in your home directory and has the correct content.
3.  **Terms of Use**: Make sure you have accepted the terms for the dataset on the CDS website.
4.  **Libraries**: Run `pip show cdsapi` to make sure the API client is installed.
