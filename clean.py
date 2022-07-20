import pandas as pd
import numpy as np
import re


def remove_emojis(string):
    characters = r'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
    for char in string:
        if char not in characters:
            string = string.replace(char, '')
    return string


# Prompt user for the years
first = int(input('Please enter the first year of your league history: '))
last = int(input('Please enter the last year of your league history: '))
folder_path = input('Please enter folder path where your csv files to clean are located (copy and paste): ')

# Create a list of the years we need to find the files for
last = last + 1
years = np.arange(2015, last)
year_list = list(years)

# Create the final dataframe with all of the cleaned data
total_data = pd.DataFrame()

for year in year_list:
    # Load the scraped csv data from a file
    df = pd.read_csv(fr'{folder_path}\{year}.csv')
    df = df.iloc[:, 1:-1]

    # Split the team member data from the Team column with regex
    df['User'] = df.apply(lambda row: re.split(r'\((.*)\)', row['Team'])[1], axis=1)
    df['Team'] = df.apply(lambda row: re.split(r'\((.*)\)', row['Team'])[0], axis=1)

    # Make sure the names in the League are all capitalized and uniform
    df['User'] = df.apply(lambda row: row['User'].title(), axis=1)

    # Remove Emojis from Team Name with the function
    df['Team'] = df.apply(lambda row: remove_emojis(row['Team']), axis=1)

    # Split the record string into three separate columns
    df['W'] = df.apply(lambda row: row['REC'].split('-')[0], axis=1)
    df['L'] = df.apply(lambda row: row['REC'].split('-')[1], axis=1)
    df['T'] = df.apply(lambda row: row['REC'].split('-')[2], axis=1)

    # Change numbers for points to a float for easier addition later
    df = df.astype({"PF": 'float', "PA": 'float'})

    # Add the Year to our entries
    df['Year'] = year

    # Rename Moves column
    df.rename(columns={'MOVES': 'Moves'}, inplace=True)

    # The final form of the dataframe that will be concated to the overall dataframe
    final_df = df.loc[:, ['User', 'RK', 'Team', 'Year', 'W', 'L', 'T', 'PF', 'PA', 'PF/G', 'PA/G', 'Moves']]

    # Concat the cleaned years dataframe to the total dataframe
    total_data = pd.concat([total_data, final_df])

# Send the total clean and merged dataframe to a csv in the folder specified above
total_data.to_csv(fr'{folder_path}\total.csv', index=False)
print('Total file successfully generated')
