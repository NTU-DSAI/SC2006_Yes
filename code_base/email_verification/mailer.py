from __future__ import annotations

'''This module contains classes which send emails.'''

__author__ = 'Loh Zhi Shen'
__verison__ = '1.0.0'
__last_updated__ = '18/08/2022'

import base64
import time
import os.path
import logging

from abc import ABC, abstractmethod
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class AbstractMailer(ABC):
    '''Abstract class for all mailers.
    
    Args:
        account (str): email of the sender.

    Notes:
        AbstractMailer does not implement send() method.
    '''
    
    def __init__(self: AbstractMailer, account: str, **kwargs: dict) -> None:
        self.__account = account

    @property
    def _account(self: AbstractMailer) -> str:
        '''str: email of the sender.'''
        return self.__account

    @abstractmethod
    def send(self: AbstractMailer, recipient: str|list[str], 
        subject: str, contents: str) -> None:
        '''Sends an email using the given account to all recipients.
        
        Args:
            recipient (str or list of str): Gmails(s) of the 
                recipient(s)
            subject (str): Subject of the email
            contents (str): Contents of the email 

        Notes:
            This method is a placeholder for individual mailers to 
            implement. 
        '''
        raise NotImplementedError

class GmailMailer(AbstractMailer):
    '''Mailer which uses a gmail account to send an email.
    
    Args:
        account (str): gmail of the sender.
        credentials (str): path to app credentials.
        token (str): path to the token.
    '''

    __SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    def __init__(self: GmailMailer, account: str, credentials: str, token: str, **kwargs: dict) -> None:
        super().__init__(account = account)
        self.__credentials = credentials
        self.__token = token

    def __authenticate(self: GmailMailer):
        """
        Retrieve user credentials.
        
        Retrieve user credentials in 1 of 3 ways:
        1. retrieve valid credentials from previous runs
        2. retrieve and refresh expired credentials from previous runs
        3. retrieves valid credentials from user login

        Returns:
            Credentials: Credentials of the user.
        """
        creds = None

        # Retrieve credentials from previous runs
        if os.path.exists(self.__token):
            creds = Credentials.from_authorized_user_file(self.__token, GmailMailer.__SCOPES)
        
        # No valid credentials available
        if not creds or not creds.valid:
            # Expired credentials
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            
            # No credentials -> create new credentials
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.__credentials, GmailMailer.__SCOPES)
                creds = flow.run_local_server(port = 0)
            
            # Save the credentials for the next run
            with open(self.__token, 'w') as token:
                token.write(creds.to_json())
        
        return creds

    def send(self: GmailMailer, recipient: str|list[str], 
        subject: str, contents: str) -> None:
        '''Sends an email using the given account to all recipients.

        Retrieve user credentials and sends a email from the 
        specified user to the specified recipient with the 
        specificed subject and contents.

        Args:
            recipient (str or list of str): Gmails(s) of the 
                recipient(s)
            subject (str): Subject of the email
            contents (str): Contents of the email  
        '''
        # Retrieve credentials
        creds = self.__authenticate()

        # Send email
        try:
            # Call the Gmail API
            service = build('gmail', 'v1', credentials = creds)

            # build the email
            message = EmailMessage()

            message['To'] = recipient
            message['From'] = super()._account
            message['Subject'] = subject

            message.set_content(contents)

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {
                'raw': encoded_message
            }

            # send the email
            (service.users()
                .messages()
                .send(userId = "me", body = create_message)
                .execute())

            # logging successful email
            t = time.localtime()
            logging.info(f'''[{t.tm_mday}/{t.tm_mon}/{t.tm_year} {t.tm_hour}{t.tm_min}] 
                Email sent from {super()._account} to {", ".join(recipient)}.''')

        except HttpError as error:
            # logging error encounted
            logging.warning(error)