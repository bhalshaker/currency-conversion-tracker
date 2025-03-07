import pandas as pd

class DatasetController():
    def get_default_dataset():
        return pd.read_csv('data/transactions.csv')