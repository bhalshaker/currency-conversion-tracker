from flask import Flask,request,jsonify
from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from controller.service_response import ServiceResponse as sr
from controller.dataset_controller import DatasetController as dc
from model.model import TransactionPath,ConvertedTransactionResponse

info = Info(title='Currency Conversion Tracker API', version='1.0.0')
app = OpenAPI(__name__, info=info)
app.json.sort_keys = False
transactions_tag = Tag(name='Transactions', description='Endpoints related to transactions')

@app.get('/transactions',
         tags=[transactions_tag],
         summary='return all converted transactions in csv',
         description='return all converted transactions in the csv file after integration with currency conversion API',
         responses={200: ConvertedTransactionResponse})
def all_trancations():
    """Apply currency conversion on full dataset of transaction"""
    df = dc.get_default_dataset()
    app.logger.info(f"data frame types {df.dtypes}")
    return jsonify(sr.response_process_data(df.to_dict(orient='records')))

@app.get('/transactions/<int:id>', tags=[transactions_tag])
def transactions_by_id(path: TransactionPath):
    """Apply currency conversion on selected transaction by id"""
    try:
        int(path.transaction_id)
    except ValueError as ve:
        return jsonify(sr.response(400, 'ERROR', 'Entered ID is not a valid base 10 number'))
    df = dc.get_default_dataset()
    filtered_df = dc.search_by_id(df, path.transaction_id)
    filtered_df = dc.prepare_df_for_integration(filtered_df)
    return jsonify(sr.response_process_data(filtered_df.to_dict(orient='records')))

@app.get('/transactions/search', tags=[transactions_tag])
def transactions_search(id: int = None):
    """Apply currency conversion on selected transaction based on applied search criteria"""
    print(id)
    return jsonify(sr.response())
# @app.route('/transactions')
# def all_trancations():
#     """Apply currency conversion on full dataset of transaction"""
#     df = dc.get_default_dataset()
#     app.logger.info(f"data frame types {df.dtypes}")
#     return jsonify(sr.response_process_data(df.to_dict(orient='records')))


# @app.route('/transactions/<id>')
# def transactions_by_id(id):
#     """Apply currency conversion on selected transaction by id"""
#     try:
#         int(id)
#     except ValueError as ve:
#         return jsonify(sr.response(500,'ERROR','Entered ID is not a valid base 10 number'))
#     df=dc.get_default_dataset()
#     filtered_df=dc.search_by_id(df,id)
#     filtered_df=dc.prepare_df_for_integration(filtered_df)
#     return jsonify(sr.response_process_data(filtered_df.to_dict(orient='records')))

# @app.route('/transactions/search')
# def transactions_search():
#     """Apply currency conversion on selected transaction based on applied search criteria"""
#     id=request.args.get('id')
#     print(id)
#     return jsonify(sr.response())

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
