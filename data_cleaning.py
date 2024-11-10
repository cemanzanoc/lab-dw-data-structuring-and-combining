#Import libraries we are working with
import pandas as pd
import numpy as np

def clean_column_names(df):
    """
    Clean column names by converting to lowercase, replacing spaces with underscores, 
    and renaming specific columns as needed (e.g., 'st' to 'state').
    
    Args:
    df (pd.DataFrame): The input dataframe whose columns need to be cleaned.
    
    Returns:
    pd.DataFrame: The dataframe with cleaned column names.
    """
    # Convert to lowercase and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    
    # Replace specific columns, like 'st' with 'state'
    df.rename(columns={'st': 'state'}, inplace=True)
    
    return df

def clean_invalid_values(df):
    """
    Clean invalid values in specified columns of the dataframe.
    
    Args:
    df (pd.DataFrame): The input dataframe with potential invalid values.
    
    Returns:
    pd.DataFrame: The dataframe with standardized values.
    """
    # Standardize Gender column
    df["gender"] = df["gender"].replace({"Femal": "F", "Male": "M", "female": "F"})
    
    # Standardize State column
    state_mapping = {
        "Cali": "California",
        "AZ": "Arizona",
        "WA": "Washington"
    }
    df["state"] = df["state"].replace(state_mapping)
    
    # Standardize Education column
    df["education"] = df["education"].replace({"Bachelors": "Bachelor"})
    
    # Standardize Customer Lifetime Value
    df['customer_lifetime_value'] = df['customer_lifetime_value'].astype(str).str.replace('%', '')
    
    # Standardize Vehicle Class column
    vehicle_mapping = {
        "Sports Car": "Luxury",
        "Luxury SUV": "Luxury",
        "Luxury Car": "Luxury",
    }
    df["vehicle_class"] = df["vehicle_class"].replace(vehicle_mapping)
    
    return df

def format_data_types(df):
    """
    Format data types of specific columns in the dataframe.
    
    Args:
    df (pd.DataFrame): The input dataframe with columns to be formatted.
    
    Returns:
    pd.DataFrame: The dataframe with formatted data types.
    """
    "------------------------------Formating Customer Lifetime Value Column------------------------------"
    # Convert Customer Lifetime Value to float
    df["customer_lifetime_value"] = df["customer_lifetime_value"].astype(float)

    "------------------------------Formating Number of Complaints Column---------------------------------"

    # Format Number of Open Complaints
    # Assuming the format is like "1/2", we will take the second value (index 1)
    #First we check if dytype is object or no
    # Check if any value contains a "/", indicating it needs splitting
    if df["number_of_open_complaints"].astype(str).str.contains("/").any():
        # Convert to string if not already and perform the split and conversion
        if df["number_of_open_complaints"].dtype != "object":
            df["number_of_open_complaints"] = df["number_of_open_complaints"].astype(str)
        
        df["number_of_open_complaints"] = df["number_of_open_complaints"].str.split("/").str[1].astype("Int64")

    else:
        # Convert to integer directly if already in the correct format
        df["number_of_open_complaints"] = df["number_of_open_complaints"].astype("Int64")
    
    return df


def handle_null_values(df):
    """
    Handle null values in the dataframe by filling them with appropriate statistics.
    
    Args:
    df (pd.DataFrame): The input dataframe with potential null values.
    
    Returns:
    pd.DataFrame: The dataframe with null values handled.
    """
    # Count the number of null values in each column
    print("Number of null values in each column before handling:")
    print(df.isna().sum())

    # Drop rows where all columns are NaN
    df = df.dropna(how='all')

    # Separate numerical and categorical columns
    numerical_columns = df.select_dtypes(include=["float64", "Int64"]).columns
    categorical_columns = df.select_dtypes(include="object").columns

    # Fill null values in numerical columns with the median
    for column in numerical_columns:
        median_value = df[column].median()
        df[column] = df[column].fillna(median_value)

    # Fill null values in categorical columns with the mode
    for column in categorical_columns:
        mode_value = df[column].mode()[0]
        df[column] = df[column].fillna(mode_value)

    # Check if there are any remaining null values
    remaining_nulls = df.isnull().sum()
    print("\nNumber of null values in each column after handling:")
    print(remaining_nulls[remaining_nulls > 0])

    return df

def handle_duplicates(df):
    """
    Identify and handle duplicate rows in the dataframe by removing them.
    
    Args:
    df (pd.DataFrame): The input dataframe with potential duplicate rows.
    
    Returns:
    pd.DataFrame: The dataframe with duplicates handled and index reset.
    """
    # Check for duplicated values
    duplicates = df.duplicated()  # Identify duplicated values
    number_of_duplicates = duplicates.sum()
    
    # Print the number of duplicated rows
    print(f"Number of duplicated rows before cleaning: {number_of_duplicates}")

    # Remove duplicates and reset index
    df_cleaned = df.drop_duplicates().reset_index(drop=True)
    
    # Check for duplicates after cleaning
    duplicates_after = df_cleaned.duplicated().sum()
    print(f"Number of duplicated rows after cleaning: {duplicates_after}")

    #Visualization optimization
    # Set the display format for floats to 2 decimal places
    pd.set_option('display.float_format', '{:.1f}'.format)
    
    return df_cleaned