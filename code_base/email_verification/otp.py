from __future__ import annotations

'''This module contains classes which generate OTPs.'''

__author__ = 'Loh Zhi Shen'
__verison__ = '1.0.1'
__last_updated__ = '18/08/2022'

import random
from time import time
from abc import ABC, abstractmethod

class AbstractOTP(ABC):
    '''Abstract class for all one-time password(OTP) generator.

    Args:
        seed (int, optional): Seed used to generate OTP.
        kwargs (dict): optional keyword arguements.

    Notes:
        AbstractOTP does not implement otp property or verify() method
    '''
    def __init__(self: AbstractOTP, seed: int | None = None, **kwargs: dict):
        if seed is not None:
            random.seed(seed)

    @abstractmethod
    def generate(self: AbstractOTP) -> str:
        '''Returns the generated OTP.

        Returns:
            str: One-time password.

        Notes:
            This is a placeholder method intended to be 
            overwritten by individual generators.
        '''
        raise NotImplementedError

    @abstractmethod
    def verify(self: AbstractOTP, otp: str) -> bool:
        '''Verifies a one-time password(OTP).
        
        Args:
            otp (str): The OTP to be verified.

        Returns:
            bool: A bool indicating whether the OTP is valid. True 
                for valid, False otherwise.

        Notes:
            This is a placeholder method intended to be 
            overwritten by individual generators.
        '''
        raise NotImplementedError

class RandomDigitOTP(AbstractOTP):
    '''One-time password(OTP) generator where OTP consist of only digits.

    Attributes:
        otp (str): OTP.

    Args:
        length (int): Length of the OTP.
        seed (int, optional): Seed used to generate OTP.
    '''

    def __init__(self: RandomDigitOTP, length: int, 
        seed: int | None = None, **kwargs: dict) -> None:

        super().__init__(seed = seed)
        self.__length = length
        self.__otp = None

    def generate(self: AbstractOTP) -> str:
        '''Returns the generated OTP.

        Returns:
            str: One-time password.
        '''

        otp = ''
        while len(otp) < self.__length:
            otp += str(random.randint(0, 9))
        self.__otp = otp

        return otp

    def verify(self: AbstractOTP, otp: str) -> bool:
        '''Verifies a one-time password(OTP).

        Args:
            otp (str): The OTP to be verified.

        Returns:
            bool: A bool indicating whether the OTP is valid. 
                True for valid, False otherwise.
        '''

        # generate() not called beforehand
        if self.__otp is None:
            return False
        # wrong OTP
        elif otp != self.__otp:
            return False

        return True

class TimedOTP(AbstractOTP):
    '''One-time password(OTP) generator wrapper which expires 
    OTPs are certain amount of time.

    Args:
        otp (AbstractOTP): OTP generator to be wrapped.
        time_limit (int): Time before OTP expires in minutes.
    '''

    # number of seconds in a minute
    __conversion_factor = 60 

    def __init__(self: TimedOTP, otp: AbstractOTP, time_limit: int, 
        **kwargs: dict) -> None:

        self.__otp = otp
        self.__time_limit = time_limit
        self.__start = None

    def generate(self: TimedOTP) -> str:
        '''Returns the generated OTP.

        Returns:
            str: One-time password.
        '''

        self.__start = time()
        return self.__otp.generate()

    def verify(self: TimedOTP, otp: str) -> bool:
        '''Verifies a one-time password(OTP).
        
        Args:
            otp (str): The OTP to be verified.

        Returns:
            bool: A bool indicating whether the OTP is valid. 
                True for valid, False otherwise.
        '''

        # generate not called beforehand
        if self.__start is None:
            return False
        # if too much time has passed since OTP was generated, OTP is no 
        # longer valid
        elif ((time() - self.__start) / TimedOTP.__conversion_factor 
            >= self.__time_limit):
            return False
        
        return self.__otp.verify(otp)
