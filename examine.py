import xarray as xr

filename = 'Merged_paralell/saudi_wind_speed_1979-1982_MERGED.nc'


# Open the dataset
ds = xr.open_dataset(filename)

# Print the dataset summary
print(ds)