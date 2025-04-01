import pandas as pd

class DatasetController():
    def get_default_dataset():
        dtype={'id': 'int64','description': 'string','amount': 'string','amount': 'float64','currency':'string','date':'string'}
        parse_dates = ['date']
        return pd.read_csv('data/transactions.csv',dtype=dtype,parse_dates=parse_dates)
    
    def search_by_id(df,id):
        return df.query('id == @id')
    
    def search_before(df,date):
        pass

    def search_after(df,date):
        pass

    def search_on(df,date):
        pass

    def search_date_interval(df,before,after):
        pass

    def search_by_term(df,search_term):
        return df.query('name.str.contains(@search_term,case=False)')

    def search_more_than(df,amount):
        return df.query('amount > @amount')

    def search_less_than(df,amount):
        return df.query('amount < @amount')
    
    def search_between_amount(df,max,min):
        return df.query('@max > age > @min')

    def search_by_currency(df,currency):
        currency_upper=currency.upper()
        return df.query('currency==@currency_upper')
        