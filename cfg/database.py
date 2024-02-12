import pyodbc 
import json

class SQLProcessingError(Exception):
    pass

class SQLDatabase():
    def __init__(self, repo, env) -> None:
        """
        Description: During __init__ SQLDataBase() object is created with correct credentials 
        Input: env -> target_branch (str)
        """
        with open('cfg/config.json') as cfg:
            try:
                self.config = json.load(cfg)[repo][env]
            except KeyError:
                self.config = json.load(cfg)[repo]['dev']


    def connect(self):
        """
        Description: Method used to connect to the database
        """
        try:
            db = self.config['database_name']
            server = self.config['database_server']
            user = self.config['user']
            password = self.config['password']

            cnxn = pyodbc.connect(
                driver ='{ODBC Driver 17 for SQL Server}', 
                server = server, 
                database = db, 
                uid = user, 
                pwd = password,
                )
            cnxn.autocommit = False
            return cnxn
        except Exception as e:
            print(e)
            return "ERROR"



