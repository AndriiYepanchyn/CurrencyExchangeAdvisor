import DataBaseApi
import requests
from dataclasses import dataclass
from datetime import datetime

class Parser:
    database_connector =""
    general_list_db_request ={} # Should return the following list of fields: date, bank_name, bank_url, bank_suffix, expected_response_format
    
    def __init__(self):
       pass
        
    def dummy_request(self):
        
        return [("NBU", 
                "https://bank.gov.ua/", 
                "/NBUStatService/v1/statdirectory/exchange?json", 
                "JSON")]
        
    def collect(self):
        print(" Parser.collect() run")
        resultset = self.dummy_request()
        print("type of rs ", type(resultset))
        for r in resultset:
            print("type of r = ", type(r))
            print("r = ", r)
            bank_name, bank_url, bank_suffix, expected_response_format = r
            url = bank_url+bank_suffix
            print("url = ", url)
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()  # JSON відповідь у словнику / списку
                for item in data:
                    print(item["cc"], item["rate"])
            else:
                print("Помилка:", response.status_code)

            
        
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
        

@dataclass
class BankConfig:
    bank_name: str
    bank_url: str
    bank_suffix: str
    expected_response_format: str
