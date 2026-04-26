from repositories.RepositoryInterface import RepositoryInterfce
import DataBaseApi

class BanksRepository(RepositoryInterfce):
    
    def __init__(self, connection :DataBaseApi):
        self.conn = connection
        
        
    # =====  Connections  =========
    def set_connection(self, connection):
        self.conn = connection
    
    
    def get_connection(self):
        return self.conn

    # ======   Getters  =========
    def get_title(self):
        return "Bank information"
    
    def get_table(self,  params=None):
        querry = "SELECT * FROM BANKS_INFO;"
        return self.conn.get_table(querry, params)
        
    def get_headers(self):
        headers, rows = self.get_table(None)
        
        return headers
    
    def get_rows(self):
        headers, rows = self.get_table(None)
       
        return rows

    def get_row(self, index):
        pass
    
    def get_rows_range(self, range_indexes):
        pass
    
    def get_value_at(self, row, col):
        pass

    # =====  Setters  =========
    def set_value_at(self, row, col, val):
        pass
        
    def set_values_at_row(self, row, data):
        pass
            
    # ======  Update  =========
    def update_params(self, new_params: dict):
        pass
    
    def insert(self, values: dict):
        bank_id = values['Bank id']
        bank_name = values['Bank name']
        bank_url =values["Bank's web page"]
        suffix = values["Suffix"]
        expected_response_format = values["Expected response format"]
                         
        print("BankRepository.insert() Data for Select")
        print(f"{bank_id};  {bank_name}; {bank_url};  {suffix}; {expected_response_format}")
        
        
        # Check if such bank already exist
        query = f"SELECT * FROM BANKS WHERE bank_id = '{bank_id}'"
        result = self.conn.fetchall(query, None)
        
        if not result: 
            insert_query = """
            INSERT INTO BANKS (bank_id, bank_name, bank_url)
            VALUES (?, ?, ?)
            """
            params = (bank_id, bank_name, bank_url)
            self.conn.execute(insert_query, params)
            
        #Check if such record already exist in the SUFFIXES
        query = f"SELECT * FROM suffixes WHERE bank_id = '{bank_id}'"
        result = self.conn.fetchall(query, None)
        
        if not result:
            insert_query = """
            INSERT INTO suffixes (suffixes_id, bank_id, suffix, expected_response_format)
            VALUES (?, ?, ?, ?)
            """
            suffixes_id = f"{bank_id}_{expected_response_format}"
            
            params = (suffixes_id, bank_id, suffix, expected_response_format)
            self.conn.execute(insert_query, params)
        else: 
            for rec in result:
                db_suffixes_id, db_bank_id, db_suffix, db_expected = rec
                eq = (db_suffix == suffix)
                print(f'Check database suffix: %s == input suffix: %s ? %s' %(db_suffix, suffix, eq) )
            
        
         
            
        print("refreshed database:")
        print('-'*80)
        res = self.conn.fetchall('SELECT * FROM BANKS_INFO;', None)
        print('BANKS_INFO_VIEW DATA = ', res)   
                 

    # =====  Delete  ==========
    def delete_row(self, row_id):
        pass
    