from abc import ABC, abstractmethod

class RepositoryInterfce(ABC):
    
    # =====  Connections  =========
    @abstractmethod
    def set_connection(self, connection):
        pass
    
    @abstractmethod
    def get_connection(self):
        pass

    # ======   Getters  =========
    @abstractmethod
    def get_title(self):
        pass
    
    @abstractmethod
    def get_table(self, params=None):
        pass
        
    @abstractmethod
    def get_headers(self):
        pass
    
    @abstractmethod
    def get_rows(self):
        pass

    @abstractmethod
    def get_row(self, index):
        pass
    
    @abstractmethod
    def get_rows_range(self, range_indexes):
        pass
    
    @abstractmethod
    def get_value_at(self, row, col):
        pass

    # =====  Setters  =========
    
    @abstractmethod
    def set_value_at(self, row, col, val):
        pass
        
    @abstractmethod
    def set_values_at_row(self, row, data):
        pass
            
    # ======  Update  =========
    
    @abstractmethod
    def update_params(self, new_params: dict):
        pass
    
    @abstractmethod
    def insert(self, values):
        pass

    # =====  Delete  ==========
    @abstractmethod
    def delete_row(self, row_id):
        pass
    