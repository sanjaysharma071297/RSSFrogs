# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 12:21:14 2020

@author: Lenovo
"""

import pyodbc
import pandas as pd



def database_connect():
    """
    Returns the connection of Sfrogs database
    Args:
    -------
        No parameters
    Returns:
    -------------
        connection of the Sfrogs Database
    """
    con = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                  'Server=sfrogs.oceanfrogs.com;'
                  'Database=Sfrogs;'
                  'uid=sf;'
                  'pwd=Sf@2020;'
                  'Trusted_Connection=no;')
    return con

def select_data_from_database(con,query):
    """
    function take SQL query and SQL connection  as input  and give the result of query as DataFrame
    Args:
    -------
        con :- SQL Connectivity from the DataBase
        query :- SQL select Query like 'select  * from table'
    Returns:
    -----------
        return table as DataFrame of sql query's result
    """
    table = pd.read_sql_query(query,con)
    return table