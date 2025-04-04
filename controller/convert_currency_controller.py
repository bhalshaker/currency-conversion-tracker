import requests
import json

def get_api_currencies():
    """Get currencies list form API"""
    currencies_request=requests.get('https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json')
    currencies_request.raise_for_status()
    return currencies_request.json()
def not_valid_currency(currency):
        return currency not in [
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
def does_currency_exists(currency,currency_list):
    """Check if currency in currency_list"""
    return currency in currency_list

def convert_currency(to_currency,from_currency,transaction_date,amount):
    """Convert from a currency to another based on date"""
    converted_amount=amount
    if from_currency.lower()!=to_currency:
        request_url=f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{transaction_date.strftime('%Y-%m-%d')}/v1/currencies/{to_currency.lower()}.json"
        convert_request=requests.get(request_url)
        convert_request.raise_for_status()
        converted_amount*=convert_request.json()[from_currency.lower()]
    return converted_amount

def dataframe_convert_currency(df):
    """Return converted dataframe"""
    df['converted_amount']=convert_currency('bhd',df['currency'],df['date'],df['amount'])
    return df