from collections import OrderedDict

class ServiceResponse():

    def response_status(code,status,message):
        return {"code":code,"status":status,"message":message}

    def response(code=500,status="ERROR",message="TECHNICAL ERROR OCCURED PLEASE TRY AGAIN",data=[]):
        return {"response status":ServiceResponse.response_status(code,status,message),"data":data}
    
    def response_process_data(data):
        if len(data)==0:
            return {"response status":ServiceResponse.response_status(204,"No content","No data found"),"data":data}
        return {"response status":ServiceResponse.response_status(202,"Accepted",f"{len(data)} RECORD(S) FOUND"),"data":data}
