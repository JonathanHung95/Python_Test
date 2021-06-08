import pandas as pd
import yaml

# read our input.yml file for the year input

with open("input.yml", "r") as f:
    data = yaml.safe_load(f)

year = data["year"]

# read the stations into memory

stations_df = pd.read_csv("Station Inventory EN.csv", skiprows = 2)

# for this exercise, we want to pull the data for Toronto City, Ontario
# so we need to identify the station id and climate id

toronto_climate_id = int(stations_df.loc[(stations_df["Name"] == "TORONTO CITY") & (stations_df["Province"] == "ONTARIO")]["Climate ID"])
toronto_station_id = int(stations_df.loc[(stations_df["Name"] == "TORONTO CITY") & (stations_df["Province"] == "ONTARIO")]["Station ID"])

print("Climate id for toronto city: ", toronto_climate_id)
print("Station id for toronto city: ", toronto_station_id)

# we use the station id to pull 3 years of climate data as requested using a shell script

data_2019_df = pd.read_csv("en_climate_daily_ON_6158355_2019_P1D.csv")
data_2020_df = pd.read_csv("en_climate_daily_ON_6158355_2020_P1D.csv")
data_2021_df = pd.read_csv("en_climate_daily_ON_6158355_2021_P1D.csv")

combined_data_df = pd.concat([data_2019_df, data_2020_df, data_2021_df])
combined_data_df.reset_index(inplace = True) 

# clean up of the data

# rows with missing mean, min and max temperature data should be removed
# could be that the data wasn't measured that day
# also because the data has entries for days that haven't occured in 2021 yet

list_to_remove = list(combined_data_df.loc[(combined_data_df["Min Temp (°C)"].isnull()) & (combined_data_df["Mean Temp (°C)"].isnull()) & (combined_data_df["Max Temp (°C)"].isnull())].index)
combined_data_df = combined_data_df.drop(list_to_remove)

# there are columns of only nulls that would be worth removing to tidy up

for i in combined_data_df.columns:
    if combined_data_df[i].isnull().sum() == len(combined_data_df):
        # if the number of nulls in the columns == the number of rows, then the whole column is empty
        # we can remove it

        del combined_data_df[i]

# merge combined_data_df with the station data given (on climate id)

new_df = combined_data_df.merge(stations_df, left_on = "Climate ID", right_on = "Climate ID")

# split up the combined dataframe based on year

new_data_2019_df = new_df[new_df["Year"] == 2019]
new_data_2020_df = new_df[new_df["Year"] == 2020]
new_data_2021_df = new_df[new_df["Year"] == 2021]

# make our neat excel file

writer = pd.ExcelWriter("climate_data.xlsx", engine = "openpyxl")
new_data_2019_df.to_excel(writer, sheet_name = "2019", index = False)
new_data_2020_df.to_excel(writer, sheet_name = "2020", index = False)
new_data_2021_df.to_excel(writer, sheet_name = "2021", index = False)
writer.close()
