import requests

def get_api_currencies():
    """Get currencies list form API"""
    currencies_request=requests.get('https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json')
    currencies_request.raise_for_status()
    return currencies_request.json()

def does_currency_exists(currency,currency_list):
    """Check if currency in currency_list"""
    return currency in currency_list