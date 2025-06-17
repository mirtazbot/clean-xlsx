import pandas as pd
import glob
import os

def sheet_split():
    xlsx = pd.ExcelFile("BU Specific - DBS.com.sg - KW Cannibalisation.xlsx")
    for sheet in xlsx.sheet_names:
        df = pd.read_excel(xlsx, sheet_name=sheet)
        df.to_csv(f"{sheet}.csv", index=False)
    print("Sheets have been split.")

dataframes = {}
def import_csv():
    file_name = []
    os.chdir(os.getcwd())
    for file in glob.glob("*.csv"):
        if file.lower() != "unwanted_data.csv":
            file_name.append(file)

    for i, fname in enumerate(file_name, start=1):
        df = pd.read_csv(fname)
        dataframes[fname] = df
        print(f"{fname}: {len(df)} rows.")

unwanted_data = [
    '\~',
    '\!',
    '\@',
    '\#',
    '\$',
    '\%',
    '\^',
    '\&',
    '\*',
    '\(',
    '\)',
    '\-',
    '\_',
    '\=',
    '\+',
    '\[',
    '\]',
    '\{',
    '\}',
    r'\\',
    '\|',
    r'\,',
    r'\"',
    '\/',
]

df0 = pd.read_csv('unwanted_data.csv')
for i in range(len(df0)):
    unwanted_data.append(df0['unwanted_data'][i])

def data_cleanup():
    for key in dataframes:
        df = dataframes[key]

        df = df[df.Clicks != 0]
        df = df[~df.Query.str.isdigit()]
        df = df[~df.Query.str.contains(r'[^\x00-\x7F]', regex=True)]
        df = df[~df.Query.str.contains(r"[a-zA-Z][.][a-zA-Z]", regex=True)]

        # Apply all unwanted patterns
        for pattern in unwanted_data:
            df = df[~df.Query.str.contains(pattern, regex=True)]

        dataframes[key] = df  # Save cleaned df back to dictionary

def export():
    # Check if 'Clean' folder exists, create if not
    os.makedirs("Clean", exist_ok=True)

    # Export each DataFrame to a CSV file
    for filename, df in dataframes.items():
        df.to_csv(f"Clean/cleaned_{filename}", index=False)

    print("Export completed.")

import_csv()
data_cleanup()
export()


