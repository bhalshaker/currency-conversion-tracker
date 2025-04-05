from flask import Flask,request,jsonify
from flask_pydantic import validate
from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from controller.service_response import ServiceResponse as sr
from controller.dataset_controller import DatasetController as dc
from controller.convert_currency_controller import dataframe_convert_currency as dcc
from model.model import TransactionPath,ConvertedTransactionResponse,SearchQueryModel,TransactionsBodyModel
import json
import pandas as pd

info = Info(title='Currency Conversion Tracker API', version='1.0.0')
app = OpenAPI(__name__, info=info)
app.json.sort_keys = False

csv_transactions_tag =Tag(name='CSV Transactions',description='Endpoints related to read transactions from CSV')
request_body_transactions_tag =Tag(name='Request Body Transactions',description='Endpoints related to read transactions from JSON Request Body')

def convert_transactions(df):
    """
    Converts transaction data in a DataFrame using an external conversion API.
    This function takes a DataFrame containing transaction data, attempts to 
    convert the transactions using the `dcc` function (presumably an API call), 
    and returns the converted data as a JSON response. If the DataFrame is empty, 
    or if an error occurs during the conversion process, appropriate error 
    responses are returned.
    Args:
        df (pandas.DataFrame): A DataFrame containing transaction data to be converted.
    Returns:
        flask.Response: A JSON response containing:
            - Converted transaction data if successful.
            - A 404 response if the DataFrame is empty.
            - A 500 response if an error occurs during the conversion process.
    Logs:
        - Logs a success message if the conversion API is called successfully.
        - Logs an error message if an exception is raised during the conversion process.
    """

    if len(df)>0:
        try:
            converted_df=dcc(df)
            app.logger.info("Successfully called conversion API to convert all transactions")
            return jsonify(sr.response_process_data(converted_df.to_dict(orient='records')))
        except Exception as e:
            app.logger.error(e)
            return jsonify(sr.response(500,'ERROR',str(e)))
            
    else:
        return jsonify(sr.response(404,'Not Found','No records to convert'))
    

@app.get('/transactions',
         tags=[csv_transactions_tag],
         summary='return all converted transactions in csv to BHD',
         description='return all converted transactions in the csv file to BHD after integration with currency conversion API',
         responses={200: ConvertedTransactionResponse})
def all_trancations():
    """
    Process and convert all transactions in the dataset to a unified currency format (BHD).

    This function retrieves the default dataset of transactions from a CSV file, applies currency 
    conversion to the entire dataset, and returns the converted data. It also handles 
    errors during dataset retrieval and logs relevant information for debugging.

    Returns:
        Response: A JSON response containing the converted transactions if successful, 
                  or an error message with a 500 status code if an exception occurs.

    Logs:
        - Logs an error message if dataset retrieval fails.
        - Logs an informational message when the dataset is successfully retrieved.
    """
    
    try:
        df = dc.get_default_dataset()
    except Exception as e:
        app.logger.error(e)
        return jsonify(sr.response(500,'ERROR',str(e)))
    app.logger.info("retrived dataset from csv file")
    return convert_transactions(df)

@app.get('/transactions/<int:id>',
         tags=[csv_transactions_tag],
         summary='Apply currency conversion on selected transaction by id to BHD',
         description='Apply currency conversion on selected transaction by id to BHD after integration with currency conversion API',
         responses={200: ConvertedTransactionResponse})
def transactions_by_id(path: TransactionPath):
    """
    Retrieve and apply currency conversion to a specific transaction by its ID.

    This function validates the provided transaction ID, retrieves the transaction
    data from the default dataset, prepares the data for integration, and applies
    currency conversion to the filtered transaction.

    Args:
        path (TransactionPath): An object containing the transaction ID to be processed.

    Returns:
        Response: A JSON response containing the converted transaction data if successful,
                  or an error message if the transaction ID is invalid or not found.

    Raises:
        ValueError: If the provided transaction ID is not a valid base-10 integer.

    Notes:
        - The function assumes the existence of a default dataset and utility functions
          for searching, preparing, and converting transaction data.
        - The response format is handled by the `sr.response` utility.
    """
  
    try:
        int(path.transaction_id)
    except ValueError as ve:
        return jsonify(sr.response(400, 'ERROR', 'Entered ID is not a valid base 10 number'))
    df = dc.get_default_dataset()
    filtered_df = dc.search_by_id(df, path.transaction_id)
    filtered_df = dc.prepare_df_for_integration(filtered_df)
    return convert_transactions(filtered_df)

@app.get('/transactions/search',
         tags=[csv_transactions_tag],
         summary='Apply currency conversion on selected transaction to BHD based on applied search criteria',
         description='Apply currency conversion on selected transaction to BHD based on applied search criteria by integration with currency conversion API',
         responses={200: ConvertedTransactionResponse})
@validate()
def transactions_search(query:SearchQueryModel):
    """
    Searches and filters transactions based on the provided query criteria, 
    applies currency conversion, and returns the filtered results.
    Args:
        query (SearchQueryModel): An object containing the search criteria, which includes:
            - after (datetime, optional): Filter transactions occurring after this date.
            - before (datetime, optional): Filter transactions occurring before this date.
            - exceed (float, optional): Filter transactions with amounts greater than this value.
            - below (float, optional): Filter transactions with amounts less than this value.
            - matching (str, optional): Filter transactions containing this term in their description or metadata.
            - currency (str, optional): Filter transactions by the specified currency.

    Returns:
        DataFrame: A DataFrame containing the filtered and currency-converted transactions.

    Notes:
        - If both `after` and `before` are provided, transactions within the date range are returned.
        - If both `exceed` and `below` are provided, transactions within the amount range are returned.
        - The function applies multiple filters sequentially based on the provided query parameters.
    """
    df = dc.get_default_dataset()
    filtered_df=df
    print(query)
    if query.after is not None and query.before is not None:
        filtered_df=dc.search_date_interval(filtered_df,query.after,query.before)
    elif query.after is not None:
        filtered_df=dc.search_after(filtered_df,query.after)
    elif query.before is not None:
        filtered_df=dc.search_before(filtered_df,query.before)
    if query.exceed is not None and query.below is not None:
        filtered_df=dc.search_between_amount(filtered_df,query.below,query.exceed)
    elif query.exceed is not None:
        filtered_df=dc.search_more_than(filtered_df,query.exceed)
    elif query.below is not None:
        filtered_df=dc.search_less_than(filtered_df,query.below)
    if query.matching is not None:
        filtered_df=dc.search_by_term(filtered_df,query.matching)
    if query.currency is not None:
        filtered_df=dc.search_by_currency(filtered_df,query.currency)
    return convert_transactions(filtered_df)
    

@app.post('/transactions',
          tags=[request_body_transactions_tag],
          summary='convert external transaction to BHD',
          description='Take posted external transaction to payload and then convert them to BHD using currency conversion API',
          responses={200: ConvertedTransactionResponse})
def process_external_transactions(body: TransactionsBodyModel):
    """
    Processes external transactions by converting the provided transaction data.
    This function takes a TransactionsBodyModel object, converts its data into a 
    DataFrame, and applies a conversion process to the transactions.
    Args:
        body (TransactionsBodyModel): The input data model containing transaction 
        details. It must not be None.
    Returns:
        DataFrame: A DataFrame containing the converted transaction data.
    Raises:
        ValueError: If the input `body` is None or invalid.
    """

    if body is not None:
        df=dc.get_json_dataset(body.model_dump_json())
        return convert_transactions(df)

@app.errorhandler(404)  
def not_found(e):
    """
    Handles 404 (Page Not Found) errors by returning a custom JSON response.

    Args:
        e (Exception): The exception object associated with the 404 error.

    Returns:
        Response: A JSON response with a 404 status code, an error message, 
                  and a description indicating that the requested URL or resource 
                  was not found.
    """
    return jsonify(sr.response(404,'NOT FOUND','Sorry, requested URL/Resource was not found!'))

@app.errorhandler(500)  
def not_found(e):
    """
    Custom error handler for 500 Internal Server Error.

    This function is triggered when an unexpected server error occurs.
    It returns a JSON response with a standardized error message.

    Args:
        e (Exception): The exception object representing the error.

    Returns:
        Response: A Flask JSON response with a 500 status code and error details.
    """
    return jsonify(sr.response(500,'ERROR',str(e)))

if __name__ == '__main__':
    app.run()
