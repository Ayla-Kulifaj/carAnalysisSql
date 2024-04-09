#importing libraries for visualization
import pandas as pd #Importing pandas library for data manipulation and analysis
import matplotlib.pyplot as plt #iImporting Matplotlib's pyplot for plotting graphs

from snowflakeConnector import SnowflakeConnector

#This line reads data from a CSV file named Automobile.csv located at the specified path and stores it in a pandas DataFrame called cars.
cars=pd.read_csv("/Users/aylakulifaj/Desktop/Project/carAnalysis/Automobile.csv")


#to see the columns names in the dataframe
print(cars.columns)

#storing car columns in a variable for usability
columnNames=cars.columns

#Prints first 5 rows 
print(cars.head())

#check for missing data
print(cars.isnull().sum()) #6 null values in horse power
#looking at basics statistics of the data frame
print(cars.describe())

# Plotting distribution of 'mpg'
#grabbing cars data frame and the MPG column to then layout a histogram
cars['mpg'].hist()
plt.title('Distribution of MPG')
plt.xlabel('MPG')
plt.ylabel('Frequency')
plt.show()
#wanted to see how many cars held the same MPG


# Plotting distribution of 'horsepower'
#grabbing cars data frame and the horsepower column to then layout a histogram
cars['horsepower'].hist()
plt.title('Distribution of Horsepower')
plt.xlabel('Horsepower')
plt.ylabel('Frequency')
plt.show()
#wanted to see how mant cars held the same horse power



#creating a condition that first goes in the dataframe cars and find which ones have 3 cylinders
condition= cars["cylinders"]==3
#removing the rows that have 3 cylinders
cars=cars.drop(cars[condition].index)

#fuel efficeny with engine size
#creating a variable and going into the cars data fram and grabbing the cylinders and mpg and finding the mean
avg_mpg_by_cyl = cars.groupby('cylinders')['mpg'].mean()
avg_mpg_by_cyl.plot(kind='bar') #bar graph
plt.title('Average MPG by Cylinders')
plt.xlabel('Cylinders')
plt.ylabel('MPG')
plt.show()



#mpg has improved over the years (model_year)
mpg_by_year = cars.groupby('model_year')['mpg'].mean()
mpg_by_year.plot()
plt.title('MPG Improvement Over Years')
plt.xlabel('Model Year')
plt.ylabel('Average MPG')
plt.show()



#Group the 'cars' DataFrame by the 'origin' column and calculate the average 'mpg' for each group
#Plot the average 'mpg' by 'origin' as a bar chart
#Set the title of the chart to 'Average MPG by Origin'
#Label the x-axis as 'Origin' and the y-axis as 'Average MPG'
#Display the bar chart
average_mpg_by_origin = cars.groupby('origin')['mpg'].mean()
average_mpg_by_origin.plot(kind='bar')
plt.title('Average MPG by Origin')
plt.xlabel('Origin')
plt.ylabel('Average MPG')
plt.show()


#Group the 'cars' DataFrame by the 'model_year' column and calculate the average 'horsepower' for each group
#Plot the average 'horsepower' by 'model_year'
#Set the title of the plot to 'Average Horsepower Over Years'
#Label the x-axis as 'Model Year' and the y-axis as 'Average Horsepower'
#Display the plot
average_hp_by_year = cars.groupby('model_year')['horsepower'].mean()
average_hp_by_year.plot()
plt.title('Average Horsepower Over Years')
plt.xlabel('Model Year')
plt.ylabel('Average Horsepower')
plt.show()

user = ""
password =""
account = ""
warehouse = "COMPUTE_WH"
database="DATA_ANALYSIS"
schema = "DATASETS"

#instantiante snowflake connection 
#con= instantiating snowflake connector class with required arguments
con=SnowflakeConnector(user=user,password=password,account=account,warehouse=warehouse,database=database,schema=schema)

#convert dataframe columns into a string

col_str = ','.join(columnNames)

#in order to insert the data  we need to create a sql insert statement
#logic to loop thru the logic for the data frame
sql = f"insert into {database}.{schema}.VEHICLE_DATA ({col_str}) VALUES "
values = ''
#for every row in the dataframe
for index, row in cars.iterrows():
    #for every value in that row
    to_add = '('
    for value in row:        
        #if value is null add sql null
        if pd.isnull(value):
            to_add += "NULL,"  # Replace NaN with NULL for SQL
            #if a column is a str we add it with quotes around it
        elif isinstance(value,str):
            to_add += f"""'{value.replace("'",'')}',"""
            #ADDING value
        else:
            to_add += f'{value},'
    #removing trailing comma
    to_add = to_add[:-1] + '),'
    #adding row to string
    values += to_add
    #taking off trailing comma and adding semicolin 
values = values[:-1] + ';'

#adds all values to sql to be ran            
sql += values

#run the SQL
con.execute(sql)



