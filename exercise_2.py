import pandas as pd
import yaml
import subprocess
import calendar
import numpy as np

# read our input.yml file for the year input

with open("input.yml", "r") as f:
    data = yaml.safe_load(f)

year = data["year"]
last_year = year - 1

# read the stations into memory

stations_df = pd.read_csv("Station Inventory EN.csv", skiprows = 2)

# for this exercise, we want to pull the data for Toronto City, Ontario
# so we need to identify the station id and climate id

toronto_climate_id = int(stations_df.loc[(stations_df["Name"] == "TORONTO CITY") & (stations_df["Province"] == "ONTARIO")]["Climate ID"])
toronto_station_id = int(stations_df.loc[(stations_df["Name"] == "TORONTO CITY") & (stations_df["Province"] == "ONTARIO")]["Station ID"])

print("Climate id for toronto city: ", toronto_climate_id)
print("Station id for toronto city: ", toronto_station_id)

# we call the shell script that contains our data download via subprocess

subprocess.call(["./get_data.sh", last_year, year])

# read the csv data generated

data_this_year_df = pd.read_csv("en_climate_daily_ON_" + str(toronto_climate_id) + "_" + str(year) + "_P1D.csv")
data_last_year_df = pd.read_csv("en_climate_daily_ON_" + str(toronto_climate_id) + "_" + str(last_year) + "_P1D.csv")

# max temperature for the year

print("Max Temperature for", year, "is (°C):", max(data_this_year_df["Max Temp (°C)"]))

# min temperature for the year

print("Minimum Temperature for", year, "is (°C):", min(data_this_year_df["Max Temp (°C)"]))

# Average temperature per month for the year
# function and iterate function to simplify things

def avg_month_temp(df, month):
    output = "The Average Temperature for " + calendar.month_abbr[month] + " is (°C): "
    average = round(df.loc[df["Month"] == month]["Mean Temp (°C)"].mean(), 2)
    output = output + str(average)

    return output

for i in range(1, 13):
    print(avg_month_temp(data_this_year_df, i))

# Average overall temperature for the year

print("Average overall temperature for", year, "is (°C):", round(data_this_year_df["Mean Temp (°C)"].mean(),2))

# number of days in this year and previous year where the temperatures were equal
# I assume that the best way to do this is to equate the mean temperatures

new_df = pd.merge(data_this_year_df, data_last_year_df, how = "inner", left_on = ["Month", "Day", "Mean Temp (°C)"], right_on = ["Month", "Day", "Mean Temp (°C)"])
print("Number of days in", year, "and", last_year, "where temperatures were equal:", len(new_df))

# number of days where they were within 1 degree of each other

combined_df = new_df = pd.merge(data_this_year_df, data_last_year_df, how = "left", left_on = ["Month", "Day"], right_on = ["Month", "Day"])
num_days = len(np.where((combined_df["Mean Temp (°C)_y"] - 1 <= combined_df["Mean Temp (°C)_x"]) & (combined_df["Mean Temp (°C)_x"] <= combined_df["Mean Temp (°C)_y"] + 1))[0])

print("Number of days in", year, "and", last_year, "where temperatures were within a degree of each other:", num_days)

