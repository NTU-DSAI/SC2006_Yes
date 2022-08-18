'''This package contains modules relate to email verification.

Usage:
from email_verification.otp import TimedOTP, RandomDigitOTP
from email_verification.mailer import GmailMailer

recipient = <<fill this in>>
subject = <<fill this in>>
contents = <<fill this in>>

OTP_METHOD = lambda x: TimedOTP(RandomDigitOTP(**x))
MAILER_METHOD = GmailMailer

# parse configs from .json file if needed
otp_config = {
    'time_limit': 1, 
    'length': 6
    }
mailer_config = {
    'account': <<email account>>, 
    'credentials': 'email_verification/credentials.json', # will upload once official app email is made 
    'token': 'email_verification/token.json' # will upload once official app email is made
    }

# create objects
otp_gen = OTP_METHOD(**otp_config)
mailer = MAILER_METHOD(**mailer_config)

# run
mailer.send(recipient = recipient, subject = subject, contents = contents.format(otp.generate()))
value = input("Enter your OTP: ")
print("Pass" if otp.verify(value) else 'Fail')
'''

__author__ = 'Loh Zhi Shen'
__verison__ = '1.0.1'
__last_updated__ = '18/08/2022'
