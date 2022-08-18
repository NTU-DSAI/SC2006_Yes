from __future__ import annotations

'''This module contains classes which generate OTPs.'''

__author__ = 'Loh Zhi Shen'
__verison__ = '1.0.0'
__last_updated__ = '18/08/2022'

import random
from time import time
from abc import ABC, abstractmethod, abstractproperty

class AbstractOTP(ABC):
    '''Abstract class for all one-time password(OTP) generator.

    Attributes:
        otp (str): OTP. 

    Args:
        seed (int, optional): Seed used to generate OTP.

    Notes:
        AbstractOTP does not implement otp property or verify() method
    '''
    def __init__(self: AbstractOTP, seed: int | None = None, **kwargs: dict):
        if seed is not None:
            random.seed(seed)

    @abstractproperty
    def otp(self: AbstractOTP) -> str:
        '''str: One-time password.

        Notes:
            This is a placeholder attribute intended to be 
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
            This is a placeholder intended to be overwritten by 
            individual generators.
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

    @property
    def otp(self: AbstractOTP) -> str:
        '''str: One-time password.'''
        otp = ''
        while len(otp) < self.__length:
            otp += str(random.randint(0, 9))
        self.__otp = otp

        return otp

    def verify(self: AbstractOTP, otp: str) -> bool:
        '''Verifies a one-time password(OTP).
        
        A OTP is valid if and only if the OTP string is correct.

        Args:
            otp (str): The OTP to be verified.

        Returns:
            bool: A bool indicating whether the OTP is valid. 
                True for valid, False otherwise.
        '''
        if self.__otp is None:
            return False
        elif otp == self.__otp:
            return True
        return False

class TimedRandomDigitOTP(RandomDigitOTP):
    '''One-time password(OTP) generator where OTP consist of only digits 
    and expires after the time limit.

    Attributes:
        otp (str): OTP.

    Args:
        time_limit (int): Time before OTP expires in minutes.
        length (int): Length of the OTP.
        seed (int, optional): Seed used to generate OTP.
    '''
    __conversion_factor = 60

    def __init__(self: TimedRandomDigitOTP, time_limit: int, 
        length: int, seed: int | None = None, **kwargs: dict) -> None:

        super().__init__(length = length, seed = seed)
        self.__time_limit = time_limit
        self.__start = None

    @property
    def otp(self: TimedRandomDigitOTP) -> str:
        '''str: One-time password.'''
        self.__start = time()
        return super().otp

    def verify(self: TimedRandomDigitOTP, otp: str) -> bool:
        '''Verifies a one-time password(OTP).

        A OTP is valid if and only if the OTP string is correct and the 
        OTP has not expired.
        
        Args:
            otp (str): The OTP to be verified.

        Returns:
            bool: A bool indicating whether the OTP is valid. 
                True for valid, False otherwise.
        '''
        # if too much time has passed since OTP was generated, OTP is no 
        # longer valid
        if self.__start is None:
            return False
        elif ((time() - self.__start) 
            / TimedRandomDigitOTP.__conversion_factor 
            >= self.__time_limit):
            return False
        
        return super().verify(otp)
