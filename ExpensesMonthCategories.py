# The script is intended to prepare a summary of expenses/income divided into categories and months.
# ver. 1.0. (19.02.2025)

import re
import pandas as pd
import csv
import os

path = input('Provide path to files: ').strip() # Getting file path

def collectFilesToLoad():
    files_to_load = {}

    while True:
        while True:  # Alias ​​validation - must be text (no numbers)
            alias = input('Enter file alias: ').strip()
            if alias and re.match(r"^[A-Za-z0-9_ -]+$", alias):  # Allowed: only letters, _, -, spaces
                break
            print('Error: Alias should only contain letters, dashes, underscores, and spaces!')

        while True:  # WFile name validation - must have .csv extension
            csv_file_to_load = input('Enter the name of the CSV file (e.g. data.csv): ').strip()
            if csv_file_to_load.lower().endswith('.csv'):
                break
            print('Error: File must have extension .csv!')

        files_to_load[alias] = csv_file_to_load  # Dodanie do słownika

        is_all_files = input('Add another file? (yes/no): ').strip().lower()
        if is_all_files not in ['YES', 'Y', 'Yes', 'yes', 'y']:
            break

    return files_to_load  # We return the entire dictionary, not a single file
files = collectFilesToLoad() # Downloading files from a user

print('Files to load: ', files)

while True: # Getting the file alias to load
    file_alias = input('Enter the alias of the file you want to load: ').strip()
    if file_alias in files:
        break
    print('Error: No such alias found! Available: ', list(files.keys()))

file_path = os.path.join(path, files[file_alias]) # Creating full path to file

try: # Loading CSV file
    df = pd.read_csv(file_path, sep=';', index_col=False)  # You can add more parameters depending on the file
    # print(df.head())  # Data preview
except FileNotFoundError:
    print(f'Error: File {file_path} does not exist!')
except Exception as e:
    print(f'An error occurred while loading the file: {e}')

def openCSVandPrintAllRows(csv_file_path):
    """ Opens CSV file and prints all rows """
    try:
        with open(csv_file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';')  # Add separator if different than standard
            for row in reader:
                print(row)
    except FileNotFoundError:
        print(f'Error: File {file_path} does not exist!')
    except Exception as e:
        print(f'An error occurred: {e}')
# openCSVandPrintAllRows(file_path) # Calling the function for the selected file
        
def printColumns(csv_files, df):
    df = pd.read_csv(csv_files, encoding="utf-8") # We load the CSV file into DataFrame
    columns_to_print = ['#Kategoria', '#Kwota'] #All columns: #Data operacji;#Opis operacji;#Rachunek;#Kategoria;#Kwota;
    columns_to_print = [col for col in columns_to_print if col in df.columns] # We check if the given columns exist in the file
    print(df[columns_to_print])
# printColumns(filesToLoad[alias], df)

def formatExpenses(df):
    df["Kwota"] = df["#Kwota"].str.replace(" PLN", "", regex=False) \
                              .str.replace(" ", "", regex=False) \
                              .str.replace(",", ".", regex=False) \
                              .astype(float)     # Converting values ​​in column "#Kwota"
    # print(df["Kwota"])
    return df  # We return the entire DataFrame with a new column "Kwota"
formatExpenses(df)

def sortByMonths(df):
    df['#Data operacji'] = pd.to_datetime(df['#Data operacji'], errors='coerce', dayfirst=True)  # Converting a column to date format if it is not already in that format
    df['Year-Month'] = df['#Data operacji'].dt.to_period('M') # Creating a "Year-Month" column in YYYY-MM format
    unique_months = df['Year-Month'].unique() # Getting unique values
    # print(unique_months)
    return unique_months

sortByMonths(df)

def sortByMonthsByCategories(df, unique_months):
    unique_categories = df["#Kategoria"].unique()
    sum_expenses = {}  # Structure: { month: { category: total } }

    for month in unique_months:
        sum_expenses[month] = {}  # We add a new entry for a given month
        for category in unique_categories:
            mask = (df['Year-Month'] == month) & (df["#Kategoria"] == category)  
            sum_expenses[month][category] = float(round(df.loc[mask, "Kwota"].sum(), 2))

    for month in sorted(sum_expenses.keys()): # Month and category sorting
        print(f"\n📅 Month: {month}")
        for category in sorted(sum_expenses[month].keys()):
            print(f"  {category}: {sum_expenses[month][category]}")

    return sum_expenses  # We return an ordered dictionary

unique_months = df['Year-Month'].unique()  # Getting unique months before using in function
results = sortByMonthsByCategories(df, unique_months) # Calling a function and writing to a function


def saveResultsToTxt(path, all_results, year, sum_expenses):
    file_path = os.path.join(path, f"{year}.txt")  

    with open(file_path, 'w', encoding='utf-8') as file:
        for month, categories in all_results.items():
            file.write(f"\n📅 {month}\n")  # New line for each month
            for category, amount in categories.items():
                if amount != 0.00: 
                    file.write(f"  {category}: {amount:.2f}\n")  # Categories in new lines

    print(f"Results save: {file_path}")
saveResultsToTxt (path, results, '2024')