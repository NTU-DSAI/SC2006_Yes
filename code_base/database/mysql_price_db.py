from __future__ import annotations

'''This module implements the SQL Price Database.'''

__author__ = 'Loh Zhi Shen'
__verison__ = '1.0.0'
__last_updated__ = '23/08/2022'

from database.price_db import PriceDB
from database.mysql import SQLDataBase

class SQLPriceDB(PriceDB):
    '''Concrete implementation of PriceDB class.

    This class functions as the interface to a SQL database which is used to store prices of the different types of hall rooms.

    Schema:
        HallId INT           : The id of the hall.
        RoomType VARCHAR(255): The type of room.
        Aircon INT           : Whether the room has aircon.
        Toilet VARChar(255)  : The type of toilet.
        Price INT            : The price of the room.

    Args:
        database_name (str): The name of the table to retrieve data from.

    Notes:
        Run the following command to generate the SQL table beforehand.

            CREATE TABLE 
                SC2006.Prices (
                    HallId INT,
                    RoomType VARCHAR(255),
                    Aircon INT,
                    Toilet VARChar(255),
                    Price INT
                )

        The following command deletes the table.

            DROP TABLE SC2006.Prices
    '''

    def __init__(self: SQLPriceDB, database_name: str) -> None:
        
        self.database_name = database_name
        self.database = SQLDataBase(database_name)

    def query(self: SQLPriceDB, hallId: int, roomType: str, aircon: bool, toilet: str, **kwarg: dict) -> int | None:
        '''Returns the price of a room given the hall id and type of room, aircon and toilet.
        
        Args:
            hallId (int)  : The id associated to a hall.

            roomType (str): The type of room. One of the following strings: "Single", "Single Plus-sized", "Double".

            aircon (bool) : A boolean indicating whether the room has aircon. True implies that the room has aircon.

            toilet (str)  : The type of toilet. One of the following strings: "Shared", "Common", "Own".
        
        Returns:
            int : The price of the room.

            None: No such room found.

        Notes:
            This command is equivalent to the following SQL query:

            SELECT 
                price
            FROM
                Prices
            WHERE
                HallId = {hallId} AND RoomType = '{roomType}' AND Aircon = {aircon} AND Toilet = '{toilet}'
            LIMIT
                1
        '''

        aircon = 1 if aircon else 0
        
        query = f"""\
            SELECT 
                price
            FROM
                Prices
            WHERE
                HallId = {hallId} AND RoomType = '{roomType}' AND Aircon = {aircon} AND Toilet = '{toilet}'
            LIMIT
                1
            """

        result = self.database.execute(query, return_result = True)
        if result is not None and len(result) > 0:
            return result[0]
        return None

    def update(self: SQLPriceDB, hallId: int, roomType: str, aircon: bool, toilet: str, price: int, **kwarg: dict) -> None:
        '''Updates the price of a room with the given hall id and type of room, aircon and toilet.
        
        Args:
            hallId (int)  : The id associated to a hall.

            roomType (str): The type of room. One of the following strings: "Single", "Single Plus-sized", "Double".

            aircon (bool) : A boolean indicating whether the room has aircon. True implies that the room has aircon.

            toilet (str)  : The type of toilet. One of the following strings: "Shared", "Common", "Own".
        
            price (int)   : The new price of the room.

        Notes:
            This command is equivalent to the following SQL query:

            UPDATE
                Prices
            SET
                Price = {price}
            WHERE
                HallId = {hallId} AND RoomType = '{roomType}' AND Aircon = {aircon} AND Toilet = '{toilet}'
        '''

        aircon = 1 if aircon else 0
        
        query = f"""\
            UPDATE
                Prices
            SET
                Price = {price}
            WHERE
                HallId = {hallId} AND RoomType = '{roomType}' AND Aircon = {aircon} AND Toilet = '{toilet}'
            """

        self.database.execute(query)
        self.database.committ()

    def insert(self: SQLPriceDB, values: list, **kwargs: dict) -> None:
        """Inserts data into the table. The order which the values should appear in the values list is: 
        (hall id, room tpye, air con, toilet, price).

        Args:
            values (list[int, str, int, str, int]): The values to insert into the table.

            hallId (int)  : The id associated to a hall.

            roomType (str): The type of room. One of the following strings: "Single", "Single Plus-sized", "Double".

            aircon (bool) : A boolean indicating whether the room has aircon. True implies that the room has aircon.

            toilet (str)  : The type of toilet. One of the following strings: "Shared", "Common", "Own".
        
        Notes:
            This command is equivalent to running the following SQL query repeatedly:

            INSERT INTO 
                Prices (HallId, RoomType, Aircon, Toilet, Price)
            VALUES 
                (%s, %s, %s, %s, %s)
        """

        query = """\
            INSERT INTO 
                Prices (HallId, RoomType, Aircon, Toilet, Price)
            VALUES 
                (%s, %s, %s, %s, %s)
            """
        if len(values) == 1:
            print(values)
        self.database.executemany(query, values)
        self.database.committ()

    def delete(self: SQLPriceDB, hallId: int, roomType: str, aircon: bool, toilet: str, **kwarg: dict) -> None:
        '''Deletes a row from the table which has the appropriate hall id and type of room, aircon, toilet.

        Args:
            hallId (int)  : The id associated to a hall.

            roomType (str): The type of room. One of the following strings: "Single", "Single Plus-sized", "Double".

            aircon (bool) : A boolean indicating whether the room has aircon. True implies that the room has aircon.

            toilet (str)  : The type of toilet. One of the following strings: "Shared", "Common", "Own".

        Notes:
            This command is equivalent to running the following SQL query repeatedly:

            DELETE FROM 
                Prices
            WHERE
                HallId = {hallId} AND RoomType = '{roomType}' AND Aircon = {aircon} AND Toilet = '{toilet}'
        '''

        query = f"""\
            DELETE FROM 
                Prices
            WHERE
                HallId = {hallId} AND RoomType = '{roomType}' AND Aircon = {aircon} AND Toilet = '{toilet}'
            """

        self.database.execute(query)
        self.database.committ()