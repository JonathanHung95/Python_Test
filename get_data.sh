#!/bin/sh

for year in `seq $1 $2`;
do for month in `seq 1 1`;
do wget --content-disposition "https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=31688&Year=${year}&Month=${month}&Day=14&timeframe=2&submit=Download+Data";
done;
done;
