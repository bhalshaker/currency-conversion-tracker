import datetime
from pydantic import BaseModel,field_validator,PositiveInt,Field
from typing import Optional,List
from controller import convert_currency_controller as ccc

class DataSetModel(BaseModel):
    id: PositiveInt
    desctiption: str
    amount: float
    currency: str
    date:str

    @field_validator('date')
    def date_in_valid_format(cls, value):
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid date format for {value}, expected format is YYYY-MM-DD")
        return value
    
    @field_validator('currency')
    def validate_currency(cls,value):
        if ccc.does_currency_exists(value):
            raise ValueError(f"{value} is not a valid currency")
        return value

class SearchQueryModel(BaseModel):
    before:Optional[str]=None
    after:Optional[str]=None
    below:Optional[float]=None
    exceed:Optional[float]=None
    matching:Optional[str]=None
    currency:Optional[str]=None

    @field_validator('currency')
    def validate_currency(cls,value):
        if ccc.does_currency_exists(value):
            raise ValueError(f"{value} is not a valid currency")
        return value
    
    @field_validator('before','after')
    def date_in_valid_format(cls, value):
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid date format for {value}, expected format is YYYY-MM-DD")
        return value

class TransactionPath(BaseModel):
    transaction_id: int = Field(alias='id', description='transaction id')

class ConvertedTransaction(DataSetModel):
    converted_amount:float

class ConvertedTransactionResponse(BaseModel):
    code: int
    status: str
    message: str
    data: List[ConvertedTransaction]


    
    