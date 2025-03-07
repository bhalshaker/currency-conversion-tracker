class ServiceResponse():
    def response_status(code=200,status='',message=''):
        return dict(code=code,status=status,message=message)
    def translated_transaction(id,description,amount,currency,date):
        return dict(id=id,description=description,amount=amount,currency=currency,date=date)
