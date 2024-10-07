import pandas as pd
import os

# Load CSV into dataframe
def get_valid_file_path():
    while True:
        # Get file path from user input
        csv_file_path = input("Please enter the full path to the CSV file: ")
        
        # Check if the file exists using os.path.exists
        if os.path.exists(csv_file_path):
            try:
                # Try reading the file into a DataFrame
                df = pd.read_csv(csv_file_path)
                return df  # Return the DataFrame if successful
            except Exception as e:
                print(f"Error reading the file: {e}")
        else:
            print(f"File does not exist: {csv_file_path}")
        print("Please try again.")

df = get_valid_file_path()

for col in df.columns:
    # Ensure that the 
    if set(df[col].unique()) == {0, 1}:
        df[col] = df[col].astype(bool)

# Function to infer SQL data types
def infer_sql_types(df):
    type_mapping = {
        'int64': 'INTEGER',
        'float64': 'FLOAT',
        'object': 'VARCHAR(255)',
        'bool': 'BOOLEAN'
    }
    
    sql_types = []
    for column in df.columns:
        # Check if the column contains only null values
        if df[column].isnull().all():
            sql_type = 'VARCHAR(255)'
        # Check if the column contains only 0 values
        elif df[column].dropna().isin([0]).all():
            sql_type = 'FLOAT'
        else:
            sql_type = type_mapping.get(str(df[column].dtype), 'VARCHAR(255)')  # Default to VARCHAR

        sql_types.append(sql_type)

    return sql_types



# Infer column names and types
column_names = df.columns.tolist()
sql_types = infer_sql_types(df)

# Create SQL "CREATE TABLE" script
table_name = 'GenericTable'
columns_with_types = ', '.join(f"{name} {sql_type}" for name, sql_type in zip(column_names, sql_types))
create_table_sql = f"CREATE TABLE {table_name} ({columns_with_types});"

# Print the SQL statement necessary to create the table
print(create_table_sql)

# Save the updated DataFrame back to the same CSV file or ask user for a new filename
save_choice = input("Do you want to overwrite the original CSV file? (y/n): ").strip().lower()

if save_choice == 'y':
    # Overwrite the original file
    df.to_csv(csv_file_path, index=False)
    print(f"CSV file successfully overwritten: {csv_file_path}")
else:
    # Ask user for new filename
    new_file_path = input("Please enter the full path for the new CSV file: ")
    df.to_csv(new_file_path, index=False)
    print(f"CSV file saved as: {new_file_path}")
