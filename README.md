# Currency Conversion Tracker

## Brief description
This project is a Flask-based web application designed to handle currency conversion for financial transactions. It provides APIs mentioned in the table below to fetch, search, and convert transaction data, leveraging external exchange rate APIs and robust data validation tools.

|Route|HTTP METHOD|Description|Parameters|
|-----|----| --------|-----|
|/transactions|GET|Apply currency conversion on all transactions|None|
|/transactions/<id>|GET|Apply currency conversion on selected transaction by id| (integer)|
|/transactions/search|GET|Apply currency conversion on selected transaction based on applied search criteria|before (YYYY-MM-DD), after (YYYY-MM-DD), below(Decimal), exceed(Decimal), match(String), currency(String)|
|/transactions|POST|Submit transaction lists to be converted|Transactions Array[id (integer), amount (Decimal), currency (String), description (String)]|

## Getting Started

To get started with the Currency Conversion Tracker project, follow these steps:

1. **Clone the Repository**:  
    Clone the project repository to your local machine:
    ```sh
    git clone https://github.com/your-username/currency-conversion-tracker.git
    cd currency-conversion-tracker
    ```

2. **Set Up the Environment** (Prefered):  
    Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:  
    Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

4. **Prepare the Data**:  
    Ensure the `data/transaction.csv` file exists and contains valid transaction data. You can use the provided sample data or create your own.
    * CSV file should contain the following fields: id,description,amount,currency,date
    * id is a postive integer.
    * description is any text.
    * amount any float/decimal amount
    * currency should be lower case and should be one of the currencies mentioned in this API: `https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json`
    * date should be in YYYY-MM-DD and later than 2024-03-31 as the used API does not provide historical exchange rates older than this date.

5. **Run the Application**:  
    Start the Flask application:
    ```sh
    flask run
    ```

6. **Access the Application**:  
    Open your web browser and navigate to `http://127.0.0.1:5000` to access the API endpoints.

7. **Test the API**:  
    Use tools like Postman or cURL to test the API routes described in the swagger ui documentation hosted on `http://localhost:5000/openapi/swagger` or through hosted documentation.

By following these steps, you will have the Currency Conversion Tracker up and running on your local machine.

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

