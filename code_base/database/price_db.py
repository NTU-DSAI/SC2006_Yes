from __future__ import annotations

"""This module contains the base class for the price database"""

__author__ = 'Loh Zhi Shen'
__verison__ = '1.0.0'
__last_updated__ = '23/08/2022'

from abc import ABC, abstractmethod

class PriceDB(ABC):
    '''Base class of the Price database system.'''

    @abstractmethod
    def query(self: PriceDB, **kwargs: dict):
        """Returns the price of a room given the hall id and type of room, aircon and toilet."""
        pass

    @abstractmethod
    def update(self: PriceDB, **kwargs: dict):
        '''Updates the price of a room with the given hall id and type of room, aircon and toilet.'''
        pass

    @abstractmethod
    def insert(self: PriceDB, **kwargs: dict):
        """Inserts data into the table."""
        pass

    @abstractmethod
    def delete(self: PriceDB, **kwargs: dict):
        '''Deletes a row from the table which has the appropriate hall id and type of room, aircon, toilet.'''
        pass

