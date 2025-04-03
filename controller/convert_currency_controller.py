import requests

def get_api_currencies():
    """Get currencies list form API"""
    currencies_request=requests.get('https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json')
    currencies_request.raise_for_status()
    return currencies_request.json()

def does_currency_exists(currency,currency_list):
    """Check if currency in currency_list"""
    return currency in currency_list

def convert_currency(to_currency,from_currency,transaction_date,amount):
    """Convert from a currency to another based on date"""
    request_url=f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{transaction_date.strftime('%Y-%m-%d')}/v1/currencies/{to_currency.lower()}.json"
    convert_request=requests.get(request_url)
    convert_request.raise_for_status()
    return convert_request.json()[from_currency.lower()]*amount