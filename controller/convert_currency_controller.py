import requests
import json

def get_api_currencies():
    """
    Fetches a list of available currencies from an external currency API.
    This function sends a GET request to the currency API endpoint to retrieve
    a JSON object containing currency codes and their corresponding names.
    Returns:
        dict: A dictionary where keys are currency codes (e.g., 'usd', 'eur') 
              and values are the names of the currencies.
    Raises:
        requests.exceptions.HTTPError: If the HTTP request to the API fails 
                                       or returns an unsuccessful status code.
    """
    
    currencies_request=requests.get('https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json')
    currencies_request.raise_for_status()
    return currencies_request.json()
def not_valid_currency(currency):
    """
    Checks if a given currency is not valid.
    This function determines whether the provided currency code is not part of 
    a predefined list of valid currency codes. The comparison is case-insensitive.
    Args:
        currency (str): The currency code to validate.
    Returns:
        bool: True if the currency is not valid (not in the list of valid currencies), 
              False otherwise.
    """
    
    return currency.lower() not in [
        "1inch", "aave", "ada", "aed", "afn", "agix", "akt", "algo", "all", "amd", "amp", "ang", "aoa", "ape", "apt", "ar", 
        "arb", "ars", "atom", "ats", "aud", "avax", "awg", "axs", "azm", "azn", "bake", "bam", "bat", "bbd", "bch", "bdt",
        "bef", "bgn", "bhd", "bif", "bmd", "bnb", "bnd", "bob", "brl", "bsd", "bsv", "bsw", "btc", "btcb", "btg", "btn", 
        "btt", "busd", "bwp", "byn", "byr", "bzd", "cad", "cake", "cdf", "celo", "cfx", "chf", "chz", "clp", "cnh", "cny", 
        "comp", "cop", "crc", "cro", "crv", "cspr", "cuc", "cup", "cve", "cvx", "cyp", "czk", "dai", "dash", "dcr", "dem", 
        "dfi", "djf", "dkk", "doge", "dop", "dot", "dydx", "dzd", "eek", "egld", "egp", "enj", "eos", "ern", "esp", "etb", 
        "etc", "eth", "eur", "fei", "fil", "fim", "fjd", "fkp", "flow", "flr", "frax", "frf", "ftt", "fxs", "gala", "gbp", 
        "gel", "ggp", "ghc", "ghs", "gip", "gmd", "gmx", "gnf", "gno", "grd", "grt", "gt", "gtq", "gusd", "gyd", "hbar", 
        "hkd", "hnl", "hnt", "hot", "hrk", "ht", "htg", "huf", "icp", "idr", "iep", "ils", "imp", "imx", "inj", "inr", 
        "iqd", "irr", "isk", "itl", "jep", "jmd", "jod", "jpy", "kas", "kava", "kcs", "kda", "kes", "kgs", "khr", "klay",
        "kmf", "knc", "kpw", "krw", "ksm", "kwd", "kyd", "kzt", "lak", "lbp", "ldo", "leo", "link", "lkr", "lrc", "lrd",
        "lsl", "ltc", "ltl", "luf", "luna", "lunc", "lvl", "lyd", "mad", "mana", "mbx", "mdl", "mga", "mgf", "mina",
        "mkd", "mkr", "mmk", "mnt", "mop", "mro", "mru", "mtl", "mur", "mvr", "mwk", "mxn", "mxv", "myr", "mzm", "mzn", 
        "nad", "near", "neo", "nexo", "nft", "ngn", "nio", "nlg", "nok", "npr", "nzd", "okb", "omr", "one", "op", "ordi",
        "pab", "paxg", "pen", "pepe", "pgk", "php", "pkr", "pln", "pte", "pyg", "qar", "qnt", "qtum", "rol", "ron", "rpl",
        "rsd", "rub", "rune", "rvn", "rwf", "sand", "sar", "sbd", "scr", "sdd", "sdg", "sek", "sgd", "shib", "shp", "sit",
        "skk", "sle", "sll", "snx", "sol", "sos", "spl", "srd", "srg", "std", "stn", "stx", "sui", "svc", "syp", "szl",
        "thb", "theta", "tjs", "tmm", "tmt", "tnd", "ton", "top", "trl", "trx", "try", "ttd", "tusd", "tvd", "twd", "twt",
        "tzs", "uah", "ugx", "uni", "usd", "usdc", "usdd", "usdp", "usdt", "uyu", "uzs", "val", "veb", "ved", "vef", "ves",
        "vet", "vnd", "vuv", "waves", "wemix", "woo", "wst", "xaf", "xag", "xau", "xaut", "xbt", "xcd", "xcg", "xch", "xdc", 
        "xdr", "xec", "xem", "xlm", "xmr", "xof", "xpd", "xpf", "xpt", "xrp", "xtz", "yer", "zar", "zec", "zil", "zmk", "zmw", 
        "zwd", "zwg", "zwl"]

def convert_currency(to_currency,from_currency,transaction_date,amount):
    """
    Converts an amount from one currency to another based on the exchange rate 
    for a given transaction date. If the exchange rate for the specified date 
    is unavailable, it falls back to the latest exchange rate.
    Args:
        to_currency (str): The target currency code (e.g., 'usd', 'eur').
        from_currency (str): The source currency code (e.g., 'usd', 'eur').
        transaction_date (datetime.date): The date of the transaction for which 
            the exchange rate is required.
        amount (float): The amount in the source currency to be converted.
    Returns:
        float: The converted amount rounded to three decimal places.
    Raises:
        requests.exceptions.HTTPError: If the HTTP request for the exchange rate 
            fails with a status code other than 404.
        KeyError: If the exchange rate for the specified currencies is not found 
            in the API response.
    Notes:
        - The function uses the currency API provided by jsDelivr to fetch 
            exchange rates.
        - Currency codes are case-insensitive.
        - If the exchange rate for the specified transaction date is unavailable, 
            the function attempts to use the latest available exchange rate.
    """
    
    converted_amount=amount
    if from_currency.lower()!=to_currency:
        request_url=f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{transaction_date.strftime('%Y-%m-%d')}/v1/currencies/{to_currency.lower()}.json"
        convert_request=requests.get(request_url)
        if convert_request.status_code==404:
            request_url=f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{to_currency.lower()}.json"
            convert_request=requests.get(request_url)
        convert_request.raise_for_status()
        exchange_rate=convert_request.json()[to_currency][from_currency.lower()]
        converted_amount/=exchange_rate
    return round(converted_amount,3)

def dataframe_convert_currency(df):
    """
    Converts the currency of amounts in a DataFrame to Bahraini Dinar (BHD).
    This function adds a new column `converted_to_bhd` to the given DataFrame.
    The new column contains the amounts converted to BHD using the `convert_currency` function.
    The conversion is performed row-wise based on the `currency`, `date`, and `amount` columns.
    Args:
        df (pandas.DataFrame): A DataFrame containing the following columns:
            - 'currency' (str): The currency code of the amount.
            - 'date' (str or datetime): The date of the conversion rate.
            - 'amount' (float): The amount to be converted.
    Returns:
        pandas.DataFrame: The input DataFrame with an additional column `converted_to_bhd` 
        containing the converted amounts in BHD.
    """
    
    new_df = df.copy()
    new_df['converted_to_bhd'] = df.apply(lambda row: convert_currency('bhd', row['currency'], row['date'], row['amount']), axis=1)
    return df