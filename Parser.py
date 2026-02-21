import DataBaseApi
import requests
from dataclasses import dataclass
from datetime import datetime

class Parser:
    database_connector =""
    general_list_db_request ={} # Should return the following list of fields: date, bank_name, bank_url, bank_suffix, expected_response_format, currency_id, rate_id
    
    def __init__(self):
       pass
        
    def dummy_request(self):
        
        return [("NBU", 
                "https://bank.gov.ua/", 
                "/NBUStatService/v1/statdirectory/exchange?json", 
                "JSON"),
                ("NBU", 
                "https://bank.gov.ua/", 
                "/NBUStatService/v1/statdirectory/exchange",
                "XML")]
        
    def collect(self):
        print(" Parser.collect() run")
        resultset = self.dummy_request()
        for r in resultset:
            bank_name, bank_url, bank_suffix, expected_response_format, currency_id, rate_id = r
            print("r = ", r)
            url = bank_url+bank_suffix
            response = requests.get(url)
            
            if response.status_code == 200:
                if(expected_response_format.upper()=="JSON"):
                    print ("JSON case started data type =")
                    data = response.json()  # JSON відповідь у словнику / списку
                    print(type(data))
                
                # if(expected_response_format.upper()=="XML"):
                #     print ("XML case started data type =")
                #     data = response.xml()  
                #     print(type(data))
                
                for item in data:
                    print(item[currency_id], item[rate_id])
                    
            else:
                print("Помилка:", response.status_code)
                
                
        self.close_connection()        

            
        
    def get_request_list_from_db(self):
        self.database_connector = DataBaseApi.DataBaseApi("sqlite")
        self.database_connector.connect()
        cursor = self.database_connector.execute(self.general_list_db_request)
        banks_info = [
                 BankConfig(*row)
                 for row in cursor.fetchall()
                 ]

        self.database_connector.close()
        return banks_info
    
    def close_connection(self):
        self.database_connector.close()
        

@dataclass
class BankConfig:
    bank_name: str
    bank_url: str
    bank_suffix: str
    expected_response_format: str
    currency_id: str
    rate_id: str
    
