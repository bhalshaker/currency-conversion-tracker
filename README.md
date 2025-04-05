# Currency Conversion Tracker

|Route|HTTP METHOD|Description|Parameters|
|-----|----| --------|-----|
|/transactions|GET|Apply currency conversion on all transactions|None|
|/transactions/<id>|GET|Apply currency conversion on selected transaction by id| (integer)|
|/transactions/search|GET|Apply currency conversion on selected transaction based on applied search criteria|before (YYYY-MM-DD), after (YYYY-MM-DD), below(Decimal), exceed(Decimal), match(String), currency(String)|
|/transactions|POST|Submit transaction lists to be converted|Transactions Array[id (integer), amount (Decimal), currency (String), description (String)]|

## Brief description
This project is a Flask-based web application designed to handle currency conversion for financial transactions. It provides APIs to fetch, search, and convert transaction data, leveraging external exchange rate APIs and robust data validation tools.
## Start Flask Application
To start the Flask application, follow these steps:

1. Ensure you have Python 3.11 installed on your system.
2. Install the required dependencies by running:
    ```sh
    pip install -r requirements.txt
    ```
3. Set the `FLASK_APP` environment variable:
    ```sh
    export FLASK_APP=app.py
    ```
4. Optionally, set the `FLASK_ENV` environment variable to `development` for debugging:
    ```sh
    export FLASK_ENV=development
    ```
5. Run the Flask application:
    ```sh
    flask run
    ```
    ## Data Folder

    Ensure that the `data` folder contains a `transaction.csv` file. This file is used to store transaction data in CSV format for processing and conversion. You can populate it with sample data or real transaction records as needed.
## Getting Started


## Technologies Used

The project leverages the following technologies and libraries:

- **Python 3.11**: The primary programming language used for building the application.
- **Flask**: A lightweight WSGI web application framework for Python.
- **pandas**: A powerful data manipulation and analysis library used to convert data from json/csv to dataframe .
- **Flask-Pydantic**: Provides Pydantic validation for Flask routes.
- **requests**: A simple HTTP library for making API calls and was used to call Currency/Exchange API.
- **flask-openapi3**: Enables OpenAPI 3.0 integration for Flask applications and enable swagger documentation ui.
- **pydantic**: Data validation and settings management using Python type annotations.
- **Currency API**: A free and open-source currency conversion API for fetching exchange rates by https://github.com/fawazahmed0/exchange-api repository .
- **pandantic**: It enables validation and filtering of pandas dataframes.

## Generate CSV file
* Currencies list https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json
