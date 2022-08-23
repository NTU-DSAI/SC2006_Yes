from __future__ import annotations

'''This module implements the SQL gateway needed by the SQL implementations of the databases.

The SQL command to create a table:
    CREATE TABLE 
        {database name}.{table name} (
            {variable name} {variable type}
        )

The SQL command to delete a table:
    DROP TABLE {database name}.{table name}
'''

__author__ = 'Loh Zhi Shen'
__verison__ = '1.0.0'
__last_updated__ = '23/08/2022'

import mysql.connector as mysql
import logging

class SQLDataBase:
    '''This class manages the SQL connection to the database and allows for the execution of a SQL query. 
    
    This class has the following roles:
        DBManager -> full rights on all databases.
        DBDesigner -> rights to create and reverse engineer any database schema.
        BackupAdmin -> minimal rights needed to backup any database.
    
    Args:
        database (str): The name of the table to retrieve data from.
    '''

    __host = 'localhost'
    __user = 'SC2006'
    __passwd = '1234'

    def __init__(self, database):

        self.database = database
        self.__db = None
        self.__cursor = None

        self.open()

    def open(self):
        """Opens the connection to the SQL server."""

        self.__error_handling(self.__open)

    def __open(self):
        """Opens the connection to the SQL server."""
    
        self.__db = mysql.connect(
            host = SQLDataBase.__host,
            user = SQLDataBase.__user,
            passwd = SQLDataBase.__passwd,
            database = self.database
        )

        self.__cursor = self.__db.cursor()

    def close(self):
        """Closes the connection to the SQL server."""

        if self.__cursor is not None:
            self.__cursor.close()
            self.__cursor = None

        if self.__db is not None:
            self.__db.close()
            self.__db = None

    def committ(self):
        """Confirms all changes to the database."""

        if self.__db is not None:
            self.__db.commit()

    def execute(self, query, return_result = False, **kwargs):
        """Calls the execute method of the cursor class.
        
        Args:
            query (str): The query to be executed.
            return_result (bool): Whether the return of the query is returned.

        Return:
            None: If return_result is False, the function returns None
            list: If return_result is True, The list of results of the query.
        """
        
        kwargs['operation'] = query
        result = self.__error_handling(self.__execute, **kwargs)
        if return_result:
            return result.fetchall()

    def __execute(self, **kwargs):
        """Calls the execute method of the cursor class."""
        
        self.__cursor.execute(**kwargs)
        return self.__cursor

    def executemany(self, query, values, return_result = False, **kwargs):
        """Calls the executemany method of the cursor class.
        
        Args:
            query (str): The query to be executed.
            values (list): Sequence of parameters for the query.
            return_result (bool): Whether the return of the query is returned.

        Return:
            None: If return_result is False, the function returns None
            list: If return_result is True, The list of results of the query.
        """
        
        kwargs['operation'] = query
        kwargs['values'] = values
        result = self.__error_handling(self.__executemany, **kwargs)
        if return_result:
            return result.fetchall()

    def __executemany(self, **kwargs):
        """Calls the executemany method of the cursor class."""

        return self.__cursor.executemany(kwargs['operation'], kwargs['values'])

    def __error_handling(self, function, **kwargs):
        '''Function wrapper to handle any SQL errors.
        
        Args:
            function (callable): The function to protect.

        Returns:
            Returns the output produced by the inputted function.
        '''

        try:

            if self.__db is None or self.__cursor is None:
                self.__open()
            if not self.__db.is_connected():
                self.__db.reconnect()

            return function(**kwargs)
        except mysql.connection.Error as err:

            logging.warning(f"""
                An error occured while connecting to SQL database:
                    {err}
                """)

            return None