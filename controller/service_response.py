from collections import OrderedDict

class ServiceResponse():

    def response_status(code,status,message):
        """
        Generate a standardized response dictionary.
        Args:
            code (int): The status code representing the outcome of an operation.
            status (str): A string indicating the status (e.g., "success", "error").
            message (str): A descriptive message providing additional details.
        Returns:
            dict: A dictionary containing the keys 'code', 'status', and 'message' with their respective values.
        """
         
        return {"code":code,"status":status,"message":message}

    def response(code=500,status="ERROR",message="TECHNICAL ERROR OCCURED PLEASE TRY AGAIN",data=[]):
        """
        Generates a standardized response dictionary for service responses.
        Args:
            code (int, optional): The HTTP status code for the response. Defaults to 500.
            status (str, optional): The status of the response, typically "SUCCESS" or "ERROR". Defaults to "ERROR".
            message (str, optional): A descriptive message providing details about the response. Defaults to "TECHNICAL ERROR OCCURED PLEASE TRY AGAIN".
            data (list, optional): The payload or additional data to include in the response. Defaults to an empty list.
        Returns:
            dict: A dictionary containing the response status and data. The "response status" key holds the result of the `ServiceResponse.response_status` method, and the "data" key holds the provided data.
        """

        return {"response status":ServiceResponse.response_status(code,status,message),"data":data}
    
    def response_process_data(data):
        """
        Processes the given data and generates a structured response.
        Args:
            data (list): A list of data items to be processed.
        Returns:
            dict: A dictionary containing:
                - "response status" (dict): The status of the response, including:
                    - HTTP status code (int)
                    - Status message (str)
                    - Additional description (str)
                - "data" (list): The original data passed to the function.
        Response Details:
            - If the input data is empty, the response status will indicate "204 No Content" 
              with a message "No data found".
            - If the input data is not empty, the response status will indicate "202 Accepted" 
              with a message specifying the number of records found.
        """

        if len(data)==0:
            return {"response status":ServiceResponse.response_status(204,"No content","No data found"),"data":data}
        return {"response status":ServiceResponse.response_status(202,"Accepted",f"{len(data)} RECORD(S) FOUND"),"data":data}
