# Python_Test
WCD python test things.

### Data Retrieval

get_data.sh is a shell script that takes 2 arguments to determine the range of years to pull from https://climate.weather.gc.ca/ . 

### Exercise_1

Python code to pull, clean and merge data from the past 3 years from the input year in the yaml file.

### Exercise_2

Python code to give:
1. Max Temperature for the year
2. Minimum Temperature for the year
3. Average Temperature for each month of the year
4. Average Temperature overall for the year
5. Number of days in this year and the previous year where:
    * Temperatures were equal
    * Temperatures were within 1 degree of each other

### Exercise_3

Dockerfile to wrap the above exercises up.  The Dockerfile builds an image using ubuntu 18.04 as a base and then executes the "run.sh" script to run the exercise_1.py and exercise_2.py files.  Console output is provided for exercise_2.

To retrieve the cleaned up "climate_data.xlsx" file from the container, run:

docker cp <container_id>:/climate_data.xlsx .

And it will pull the file from the container, regardless of whether it's currently running or not.