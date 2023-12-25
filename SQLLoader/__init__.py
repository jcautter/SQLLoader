from SQLServer import SQLServer
import pandas as pd

class SQLLoader:
    
    def __init__(self, df, query, dns, database_name, port_number=None, user_id=None, password=None, chunk=False, dates_field:list=None, query_truncate=None, func=None):
        self.connect(dns, database_name, port_number, user_id, password)
        if query_truncate:
            self.server.execute_query(query_truncate, True)
        if chunk:
            for c in df:
                self.parm = self.trait(c, func=func)
                self.server.insert_many(query, self.parm)
        else:
            self.parm = self.trait(df, func=func)
            self.res = self.server.insert_many(query, self.parm)
    
    def connect(self, dns, database_name, port_number, user_id, password):
        self.server = SQLServer(dns, database_name, port_number, user_id, password)
        
    def trait(self, df, dates_field:list=None, func=None):
        if dates_field:
            for f in dates_field:
                if f in df.columns:
                    df = self.trait_date(df, f)
        if func:
            df = func(df)
        return self.get_parms(df)
    
    def trait_date(self, df, field_name):
        return df.assign(
            **{
                field_name: lambda x: x[field_name].dt.strftime('%Y-%m-%d')
            }
        )
    
    def get_parms(self, df):
        return [
            tuple([
                None if type(val) in [float, int] and np.isnan(val) else val 
                for val in a[1].to_dict().values()]) 
            for a in df.iterrows()
        ]
