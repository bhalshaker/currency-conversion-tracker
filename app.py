from flask import Flask,request,jsonify
from controller.service_response import ServiceResponse as sr
from controller.dataset_controller import DatasetController as dc

app = Flask(__name__)
app.json.sort_keys = False

@app.route('/transactions')
def all_trancations():
    df = dc.get_default_dataset()
    app.logger.info(f"data frame types {df.dtypes}")
    return jsonify(sr.response_process_data(df.to_dict(orient='records')))

@app.route('/transactions/upload',methods=['POST'])
def upload_transactions():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    return jsonify(sr.response(200,'SUCCESSFUL','File was upload successfuly'))


@app.route('/transactions/<id>')
def transactions_by_id(id):
    try:
        int(id)
    except ValueError as ve:
        return jsonify(sr.response(500,'ERROR','Entered ID is not a valid base 10 number'))
    df=dc.get_default_dataset()
    filtered_df=dc.search_by_id(df,id)
    return jsonify(sr.response_process_data(filtered_df.to_dict(orient='records')))

@app.route('/transactions/search')
def transactions_search():
    id=request.args.get('id')
    print(id)
    return jsonify(sr.response())

@app.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e):
    return jsonify(sr.response(404,'NOT FOUND','Sorry, requested URL/Resource was not found!'))

@app.errorhandler(500) 
# inbuilt function which takes error as parameter 
def not_found(e):
    return jsonify(sr.response(500,'ERROR','Sorry, an expected technical error occured!'))

if __name__ == '__main__':
    app.run()
