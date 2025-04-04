import datetime
from datetime import date
from pydantic import BaseModel,field_validator,PositiveInt,Field, model_validator
from typing import Optional,List,Literal,Any
from controller import convert_currency_controller as ccc

class TransactionModel(BaseModel):
    id: int
    description: str
    amount: float
    currency: Literal[
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
    date: date

class SearchQueryModel(BaseModel):
    before:Optional[date]=None
    after:Optional[date]=None
    below:Optional[float]=None
    exceed:Optional[float]=None
    matching:Optional[str]=None
    currency: Literal[
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
          "zwd", "zwg", "zwl"]=None

    @field_validator('currency')
    def validate_currency(cls,value):
        if ccc.not_valid_currency(value):
            raise ValueError(f"{value} is not a valid currency")
        return value
    
    @field_validator('before','after')
    def date_in_valid_format(cls, value):
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid date format for {value}, expected format is YYYY-MM-DD")
        return value
    
    @model_validator(mode='before')
    @classmethod
    def check_amount_between_inputs(cls, data: Any) -> Any:  
        if isinstance(data, dict):  
            if data.below is not None and data.exceed is not None: 
                if (data.exceed>=data.below):
                    raise ValueError("exceed should be less than and should not equal to below")
        return data
    
    @model_validator(mode='before')
    @classmethod
    def check_date_between_inputs(cls, data: Any) -> Any:  
        if isinstance(data, dict):  
            if data.before is not None and data.after is not None: 
                if (data.after>=data.before):
                    raise ValueError("after should be less than and should not equal to before")
        return data

class TransactionPath(BaseModel):
    transaction_id: int = Field(alias='id', description='transaction id')

class ConvertedTransaction(TransactionModel):
    converted_amount:float

class ConvertedTransactionResponse(BaseModel):
    code: int
    status: str
    message: str
    data: List[ConvertedTransaction]

class TransactionsBodyModel(BaseModel):
    data:List[TransactionModel]


    
    