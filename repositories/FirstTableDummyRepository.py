from repositories.RepositoryInterface import RepositoryInterfce


class FirstTableDummyRepository(RepositoryInterfce) :

    def __init__(self, connection):
        self.conn = connection
     

    
    # =====  Connections  =========
    def set_connection(self, connection):
        pass
    
    def get_connection(self):
        pass

    # ======   Getters  =========
    def get_title(self):
        return "Dummy table"
    
    def get_table(self,  params=None):
        pass
    
    def get_headers(self):
        data = ("Bank", "Buy rate", "Sell rate")
        return data    
    
    def get_rows(self):
        data = [
            ("PrivatBank", "39.3000", "40.1000"),
            ("MonoBank", "39.4500", "40.1500"),
            ("OschadBank", "39.2000", "40.0500"),
            ("PUMB", "39.3800", "40.0900")
        ]
        return  data       

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
    