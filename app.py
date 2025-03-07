from flask import Flask,request,jsonify
from controller.service_response import ServiceResponse as sr

app = Flask(__name__)

@app.route('/transactions')
def all_trancations():
    return 'Hello World'

@app.route('/transactions/<id>')
def transactions_by_id(id):
    try:
        int(id)
    except ValueError as ve:
        return jsonify(sr.response_status(500,'ERROR','Entered ID is not a valid base 10 number'))
    return jsonify(sr.response_status())

@app.route('/transactions/search')
def transactions_search():
    id=request.args.get('id')
    print(id)
    return jsonify(sr.response_status())

if __name__ == '__main__':
    app.run(debug=True)
