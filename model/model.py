import datetime
from datetime import date
from pydantic import BaseModel,field_validator,PositiveInt,Field, model_validator
from typing import Optional,List,Literal,Any
from controller import convert_currency_controller as ccc

class TransactionModel(BaseModel):
    """
    TransactionModel represents a financial transaction with details such as 
    an identifier, description, amount, currency, and date.
    Attributes:
        id (int): A unique identifier for the transaction.
        description (str): A brief description of the transaction.
        amount (float): The monetary value of the transaction.
        currency (Literal): The currency code for the transaction, 
            which must be one of the predefined values (e.g., "usd", "eur", "btc").
        date (date): The date of the transaction. Must be greater than 2024-04-01.
    Methods:
        validate_date(cls, value): Validates that the date is greater than 2024-04-01.
            Raises:
                ValueError: If the date is not greater than 2024-04-01.
    """

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

    @field_validator('date')
    def validate_date(cls, value):
        """
        Validates that the provided date is greater than April 1, 2024.
        Args:
            value (date): The date to validate.
        Returns:
            date: The validated date if it meets the condition.
        Raises:
            ValueError: If the provided date is less than or equal to April 1, 2024.
        """

        if value <= date(2024, 3, 31):
            raise ValueError("Date must be greater than 2024-04-01")
        return value

class SearchQueryModel(BaseModel):
    """
    SearchQueryModel is a Pydantic model that represents a search query with various optional filters.
    Attributes:
        before (Optional[date]): A date filter to specify the upper limit of a date range.
        after (Optional[date]): A date filter to specify the lower limit of a date range.
        below (Optional[float]): A numeric filter to specify the upper limit of a value range.
        exceed (Optional[float]): A numeric filter to specify the lower limit of a value range.
        matching (Optional[str]): A string filter for matching specific text.
        currency (Literal): A literal type representing a list of supported currency codes.
    Validators:
        - check_amount_between_inputs: Ensures that the 'exceed' value is less than the 'below' value.
        - check_date_between_inputs: Ensures that the 'after' date is less than the 'before' date.
        - check_all_fields_not_null: Ensures that at least one field in the model is provided.
    """

    before: Optional[date] = None
    after: Optional[date] = None
    below: Optional[float] = None
    exceed: Optional[float] = None
    matching: Optional[str] = None
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
        "zwd", "zwg", "zwl"] = None

    @model_validator(mode='before')
    @classmethod
    def check_amount_between_inputs(cls, data: Any) -> Any:
        """
        Validates that the 'exceed' value in the input data is less than the 'below' value.
        This method checks if the input data is a dictionary and contains the keys 'below' and 'exceed'.
        If both keys are present, it ensures that the integer value of 'exceed' is strictly less than
        the integer value of 'below'. If this condition is not met, a ValueError is raised.
        Args:
            data (Any): The input data to validate. Expected to be a dictionary containing 'below' 
                        and 'exceed' keys.
        Returns:
            Any: The original input data if validation passes.
        Raises:
            ValueError: If 'exceed' is greater than or equal to 'below'.
        """

        if isinstance(data, dict):
            if data.get('below') is not None and data.get('exceed') is not None:
                if int(data.get('exceed')) >= int(data.get('below')):
                    raise ValueError("exceed should be less than and should not equal to below")
        return data

    @model_validator(mode='before')
    @classmethod
    def check_date_between_inputs(cls, data: Any) -> Any:
        """
        Validates that the 'after' date is strictly less than the 'before' date in the provided data.
        Args:
            data (Any): The input data, expected to be a dictionary containing 'before' and 'after' keys.
        Returns:
            Any: The original input data if validation passes.
        Raises:
            ValueError: If the 'after' date is greater than or equal to the 'before' date.
        """

        if isinstance(data, dict):
            if data.get('before') is not None and data.get('after') is not None:
                if date(data.get('after')) >= date(data.get('before')):
                    raise ValueError("after should be less than and should not equal to before")
        return data

    @model_validator(mode='before')
    @classmethod
    def check_all_fields_not_null(cls, data: Any) -> Any:
        """
        Validates that at least one field in the provided data is not null.
        Args:
            data (Any): The input data to validate. Expected to be a dictionary.
        Returns:
            Any: The input data if validation passes.
        Raises:
            ValueError: If all fields in the dictionary are None.
        """

        if isinstance(data, dict):
            if all(value is None for value in data.values()):
                raise ValueError("At least one field must be provided")
        return data

class TransactionPath(BaseModel):
    """
    TransactionPath is a model representing the path of a transaction.
    Attributes:
        transaction_id (int): The unique identifier for the transaction. 
            This field is aliased as 'id' and includes a description for clarity.
    """

    transaction_id: int = Field(alias='id', description='transaction id')

class ConvertedTransaction(TransactionModel):
    """
    ConvertedTransaction is a subclass of TransactionModel that represents a transaction
    with an additional field for the amount converted to Bahraini Dinar (BHD).
    Attributes:
        converted_to_bhd (float): The amount of the transaction converted to Bahraini Dinar.
    """

    converted_to_bhd:float

class ConvertedTransactionResponse(BaseModel):
    """
    ConvertedTransactionResponse is a Pydantic model that represents the response structure
    for a converted transaction. It includes the following attributes:
    Attributes:
        code (int): The status code of the response.
        status (str): The status of the response, typically indicating success or failure.
        message (str): A descriptive message providing additional information about the response.
        data (List[ConvertedTransaction]): A list of converted transaction objects containing
            detailed information about the transactions.
    """
    
    code: int
    status: str
    message: str
    data: List[ConvertedTransaction]

class TransactionsBodyModel(BaseModel):
    """
    TransactionsBodyModel represents the structure of a request or response body
    that contains a list of transactions.
    Attributes:
        transactions (List[TransactionModel]): A list of transaction objects, 
        where each transaction is represented by an instance of TransactionModel.
    """

    transactions:List[TransactionModel]


    
    