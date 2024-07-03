import pyodbc

def get_db_connection():
    connection = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=minhhoa;'
        'DATABASE=nhahang;'
        'UID=sa;'
        'PWD=123'
    )
    return connection
