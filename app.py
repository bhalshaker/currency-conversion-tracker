from flask import Flask,request,jsonify
from flask_pydantic import validate
from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from controller.service_response import ServiceResponse as sr
from controller.dataset_controller import DatasetController as dc
from controller.convert_currency_controller import dataframe_convert_currency as dcc
from model.model import TransactionPath,ConvertedTransactionResponse,SearchQueryModel,TransactionsBodyModel

info = Info(title='Currency Conversion Tracker API', version='1.0.0')
app = OpenAPI(__name__, info=info)
app.json.sort_keys = False
csv_transactions_tag =Tag(name='CSV Transactions',description='Endpoints related to read transactions from CSV')
request_body_transactions_tag =Tag(name='Request Body Transactions',description='Endpoints related to read transactions from JSON Request Body')

@app.get('/transactions',
         tags=[csv_transactions_tag],
         summary='return all converted transactions in csv',
         description='return all converted transactions in the csv file after integration with currency conversion API',
         responses={200: ConvertedTransactionResponse})
def all_trancations():
    """Apply currency conversion on full dataset of transaction"""
    try:
        df = dc.get_default_dataset()
    except Exception as e:
        app.logger.error(e)
        return jsonify(sr.response_status(500,'ERROR','Structure of CSV data is not as per standard please refer to the documentation to fix the issue'))
    app.logger.info("retrived dataset from csv file")
    try:
        converted_df=dcc(df)
        app.logger.info("Successfully called conversion API to convert all transactions")
    except Exception as e:
        app.logger.error(e)
        return jsonify(sr.response_status(500,'ERROR','ERROR Occured while trying to convert the transaction through the API'))
    return jsonify(sr.response_process_data(converted_df.to_dict(orient='records')))

@app.get('/transactions/<int:id>',
         tags=[csv_transactions_tag],
         summary='Apply currency conversion on selected transaction by id',
         description='Apply currency conversion on selected transaction by id after integration with currency conversion API',
         responses={200: ConvertedTransactionResponse})
def transactions_by_id(path: TransactionPath):
    """Apply currency conversion on selected transaction by id"""
    try:
        int(path.transaction_id)
    except ValueError as ve:
        return jsonify(sr.response(400, 'ERROR', 'Entered ID is not a valid base 10 number'))
    df = dc.get_default_dataset()
    filtered_df = dc.search_by_id(df, path.transaction_id)
    filtered_df = dc.prepare_df_for_integration(filtered_df)
    try:
        converted_df=dcc(filtered_df)
        app.logger.info("Successfully called conversion API to convert all transactions")
    except Exception as e:
        app.logger.error(e)
        return jsonify(sr.response_status(500,'ERROR','ERROR Occured while trying to convert the transaction through the API'))
    return jsonify(sr.response_process_data(converted_df.to_dict(orient='records')))

@app.get('/transactions/search',
         tags=[csv_transactions_tag],
         summary='Apply currency conversion on selected transaction based on applied search criteria',
         description='pply currency conversion on selected transaction based on applied search criteria by integration with currency conversion API',
         responses={200: ConvertedTransactionResponse})
@validate()
def transactions_search(query:SearchQueryModel):
    """Apply currency conversion on selected transaction based on applied search criteria"""
    print(id)
    return jsonify(sr.response())

@app.post('/transactions',
          tags=[request_body_transactions_tag],
          summary='',
          description='',
          responses={200: ConvertedTransactionResponse})
def process_external_transactions(body: TransactionsBodyModel):
    pass

@app.errorhandler(404)  
def not_found(e):
    """Customize in built 404 error (PAGE NOT FOUND) handler"""
    return jsonify(sr.response(404,'NOT FOUND','Sorry, requested URL/Resource was not found!'))

@app.errorhandler(500)  
def not_found(e):
    """Customize in built 500 error (Server Error) handler"""
    return jsonify(sr.response(500,'ERROR','Sorry, an expected technical error occured!'))

if __name__ == '__main__':
    app.run()
