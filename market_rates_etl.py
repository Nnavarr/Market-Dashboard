import pandas as pd
import numpy as np
import datetime
import os
import win32com.client
import rate_processing

"""
Author: Noe Navarro
Date: 11/4/2020
Objective:
    Automatically download Excel spreadsheet from Outlook email to be
    processed and prepared for powering the Market Dashboard

Update Log
----------
Version 0.1.0: Inception of life | 11/4/2020 | NN
"""

def download_attachment(save_path):
    """
    Author: Noe Navarro
    Date: 11/9/2020

    param1: save_path; location where the master rate file is to be saved
    return: NA; downloads the latest Excel attachment
    """

    # establish download parameters
    today = datetime.date.today()

    # Outlook needs to be closed in order for this to run properly
    outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')
    inbox = outlook.Folders.Item(1).Folders['Market Rates'].Items

    # date parameters for email processing
    today = datetime.date.today()
    yesterday = today + datetime.timedelta(days=-1)

    # extract attachment if criteria is met
    for email in inbox:
        # convert date sent to pd datetime for comparison
        if (pd.to_datetime(email.SentOn.strftime(format='%Y-%m-%d')) >= yesterday) & ('Market Rate' in email.Subject):
            attachment = email.Attachments.item(1)
            attachment.SaveAsFile(save_path + '\\market_rates.xlsx')
        else:
            pass

def data_processing(save_path):

    try:
        download_attachment(save_path)
        rate_processing.main()
        print('Data processed successfully!')
    except:
        print('There was an error in the data processing')


if __name__ == '__main__':
    save_path = r'C:\Users\Noe_N\OneDrive\Market Data\market_dashboard\market_data'
    data_processing(save_path)
