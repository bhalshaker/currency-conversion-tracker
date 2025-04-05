import pandas as pd
import json
from pandantic import Pandantic
from model.model import TransactionModel

class DatasetController():
    def get_default_dataset():
        """
        Reads a CSV file containing transaction data, validates it against a schema, 
        and processes the data for further use.
        Returns:
            pandas.DataFrame: A DataFrame containing the processed transaction data.
        Steps:
            1. Reads the 'data/transactions.csv' file into a DataFrame with specified data types.
            2. Validates the DataFrame against the TransactionModel schema using Pandantic.
            3. Converts the 'currency' column values to lowercase.
            4. Converts the 'date' column to datetime format.
        Raises:
            ValidationError: If the DataFrame does not conform to the TransactionModel schema.
        """

        validator = Pandantic(schema=TransactionModel)
        dtype={'id': 'int64','description': 'string','amount': 'float64','currency':'string','date':'string'}
        df=pd.read_csv('data/transactions.csv',dtype=dtype)
        validator.validate(dataframe=df, errors="raise")
        df['currency'].apply(lambda x: x.lower())
        df['date'] = pd.to_datetime(df['date'])
        return df
    
    def get_json_dataset(json_data):
        """
        Converts a JSON string containing transaction data into a pandas DataFrame.
        Args:
            json_data (str): A JSON-formatted string containing transaction data. 
                             The JSON object is expected to have a 'transactions' key 
                             which maps to a list of transaction records.
        Returns:
            pandas.DataFrame: A DataFrame containing the transaction data with the following columns:
                - 'description' (string): Description of the transaction.
                - 'amount' (float64): Amount of the transaction.
                - 'currency' (string): Currency of the transaction.
                - 'date' (datetime64): Date of the transaction.
        Raises:
            KeyError: If the 'transactions' key is missing in the JSON data.
            ValueError: If the 'date' column cannot be converted to datetime format.
        Example:
            json_data = '{"transactions": [{"description": "Payment", "amount": 100.0, "currency": "USD", "date": "2023-01-01"}]}'
            df = get_json_dataset(json_data)
            print(df)
        """

        data = json.loads(json_data)
        transactions = data['transactions']
        df=pd.DataFrame(transactions)
        df['description'] = df['description'].astype("string")
        df['amount'] = df['amount'].astype("float64")
        df['currency'] = df['currency'].astype("string")
        print(df.dtypes)
        df['date'] = pd.to_datetime(df['date'])
        return df

    
    def search_by_id(df,id):
        """
        Search for rows in a DataFrame where the 'id' column matches the given value.
        Args:
            df (pandas.DataFrame): The DataFrame to search within.
            id (int or str): The value to match in the 'id' column.
        Returns:
            pandas.DataFrame: A DataFrame containing rows where the 'id' column matches the given value.
        """

        return df.query('id == @id')
    
    def search_before(df,date):
        date = pd.to_datetime(date)
        print(type(date))
        return df[df['date'] < '2025-03-01']

    def search_after(df,date):
        date = pd.to_datetime(date)
        print(date)
        return df.query('date > @date')

    def search_on(df,date):
        return df.query('date == @date')

    def search_date_interval(df,before,after):
        return df.query('@before < date < @after')

    def search_by_term(df,search_term):
        return df.query('name.str.contains(@search_term,case=False)')

    def search_more_than(df,amount):
        return df.query('amount > @amount')

    def search_less_than(df,amount):
        return df.query('amount < @amount')
    
    def search_between_amount(df,max,min):
        return df.query('@max > amount > @min')

    def search_by_currency(df,currency):
        currency_lower=currency.lower()
        return df.query('currency==@currency_lower')
    
    def prepare_df_for_integration(df):
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
        return df
        