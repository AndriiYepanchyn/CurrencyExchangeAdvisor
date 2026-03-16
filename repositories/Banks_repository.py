from repositories.RepositoryInterface import RepositoryInterfce
import DataBaseApi

class Banks_repository(RepositoryInterfce):
    
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
    
    def insert(self, values):
        pass

    # =====  Delete  ==========
    def delete_row(self, row_id):
        pass
    