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
            pandas.DataFrame: Transactions DataFrame containing the processed transaction data.
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
            pandas.DataFrame: Transactions DataFrame containing the transaction data with the following columns:
                - 'description' (string): Description of the transaction.
                - 'amount' (float64): Amount of the transaction.
                - 'currency' (string): Currency of the transaction in small letters.
                - 'date' (datetime64): Date of the transaction.
        Raises:
            KeyError: If the 'transactions' key is missing in the JSON data.
            ValueError: If the 'date' column cannot be converted to datetime format.
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

        return df.query('`id` == @id')
    
    def search_before(df,date):
        """
        Filters a DataFrame to return rows where the 'date' column is earlier than the specified date.
        Args:
            df (pandas.DataFrame): The DataFrame to filter. Must contain a 'date' column.
            date (datetime-like): The date to compare against. Rows with 'date' values earlier than this will be returned.
        Returns:
            pandas.DataFrame: A filtered DataFrame containing rows where the 'date' column is earlier than the specified date.
        """

        print(type(date))
        return df.query('`date` < @date')

    def search_after(df,date):
        """
        Filters transactions DataFrame to include only rows where the 'date' column is greater than the specified date.
        Args:
            df (pandas.DataFrame): Transactions DataFrame to filter. It must contain a column named 'date'.
             date (datetime or str): The date to compare against. Rows with a 'date' value greater than this will be included.
        Returns:
            pandas.DataFrame: A filtered DataFrame containing rows where the 'date' column is greater than the specified date.
        """
        
        print(type(date))
        return df.query('`date` > @date')

    def search_date_interval(df,after,before):
        """
        Filters transactions DataFrame to include only rows where the 'date' column falls 
        within the specified interval (exclusive).
        Args:
            df (pandas.DataFrame): Transaction DataFrame to filter. Must contain a 'date' column.
            after (datetime-like): The lower bound of the date interval (exclusive).
            before (datetime-like): The upper bound of the date interval (exclusive).

        Returns:
            pandas.DataFrame: Filtered transactions DataFrame containing rows where the 'date' 
            column is greater than `after` and less than `before`.
        """
        return df.query('@after < `date` < @before')

    def search_by_term(df,search_term):
        """
        Filters transactions DataFrame to return rows where the 'description' column contains the specified search term, 
        ignoring case.
        Args:
            df (pandas.DataFrame): Transactions DataFrame to search within. It must have a column description 'description'.
            search_term (str): The term to search for within the 'description' column.
        Returns:
            pandas.DataFrame: Filtered transactions DataFrame containing rows where the 'description' column matches 
            the search term.
        """
        
        return df.query('description.str.contains(@search_term,case=False)')

    def search_more_than(df,amount):
        """
        Filters a DataFrame to return rows where the 'amount' column has values greater than the specified amount.
        Args:
            df (pandas.DataFrame): Transactions to filter. It must contain a column named 'amount'.
            amount (float or int): The threshold value to filter rows.
        Returns:
            pandas.DataFrame: Filtered transactions DataFrame containing rows where the 'amount' column is greater than the specified value.
        """

        return df.query('`amount` > @amount')

    def search_less_than(df,amount):
        """
        Filters transactions DataFrame to return rows where the 'amount' column is less than the specified value.
        Args:
            df (pandas.DataFrame): Transactions DataFrame to filter. It must contain a column named 'amount'.
            amount (float or int): The threshold value to filter rows.
        Returns:
            pandas.DataFrame: Filtered transactions DataFrame containing rows where the 'amount' column is less than the specified value.
        """
        
        return df.query('`amount` < @amount')
    
    def search_between_amount(df,max,min):
        """
        Filters transactions DataFrame to return rows where the 'amount' column values 
        are between the specified maximum and minimum values.
        Args:
            df (pandas.DataFrame): Transactions DataFrame to filter. Must contain a column named 'amount'.
            max (float): The upper bound for the 'amount' column values.
            min (float): The lower bound for the 'amount' column values.
        Returns:
            pandas.DataFrame: Filtered transactions DataFrame containing rows where the 'amount' 
            column values are greater than 'min' and less than 'max'.
        """

        return df.query('@max > `amount` > @min')

    def search_by_currency(df,currency):
        """
        Filters transaction DataFrame to return rows where the 'currency' column matches the specified currency.
        Args:
            df (pandas.DataFrame): Transactions DataFrame to search within. It must contain a column named 'currency'.
            currency (str): The currency value to search for. The search is case-insensitive.
        Returns:
            pandas.DataFrame: Transactions DataFrame containing rows where the 'currency' column matches the specified currency.
        """

        currency_lower=currency.lower()
        return df.query('`currency`==@currency_lower')
    
    def prepare_df_for_integration(df):
        """
        Prepares transactions DataFrame for integration by converting the 'date' column 
        to a datetime object.
        Args:
            df (pd.DataFrame): Transactions DataFrame containing a 'date' column 
            with string values in the format '%Y-%m-%d'.
        Returns:
            pd.DataFrame: The modified transactions DataFrame with the 'date' column 
            converted to datetime. Invalid parsing will result in NaT (Not a Time).
        """

        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
        return df
        