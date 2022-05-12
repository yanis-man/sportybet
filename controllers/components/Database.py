import mysql.connector as mySQL

class Database:

    def __init__(self) -> None:
        self.database = mySQL.connect(host="localhost", user="root", password="root", database="sportbet")

    def save_to_db(self, QUERY: str, params : tuple):
        cursor = self.database.cursor() 
        cursor.execute(QUERY, params)
# utilitary function to execute a query which pulls from the DB
    def pull_from_db(self, QUERY : str, params : tuple = (), only_first = False, order_by = None):
        cursor = self.database.cursor()
        query = QUERY
        if order_by is not None:
            query = f'{QUERY} ORDER BY {order_by} ASC'

        cursor.execute(query, params)
        
        if only_first:
            return cursor.fetchone()
        
        return cursor.fetchall()

