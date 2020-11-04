import numpy as np
import pandas as pd
import re

"""
Initial Import and Cleaning
    This portion of the script will clean the relevant data from Mason B.'s
    excel spreadsheet. From here, we can append rate into an external
    reference (SQL) db
"""
def read_spreadsheet(sheet, other_rates=False):

    if other_rates is True:
        df = pd.read_excel(r'C:\Users\Noe_N\OneDrive\Market Data\market_dashboard\market_data\market_rates.xlsx',
                                       sheet_name=sheet,
                                       header=4)
    else:
        df = pd.read_excel(r'C:\Users\Noe_N\OneDrive\Market Data\market_dashboard\market_data\market_rates.xlsx',
                           sheet_name=sheet,
                           header=2)
    return df

def other_rate_clean(df, prime=True):

    # prime rate clean ----
    if prime is True:
        df.dropna(inplace=True)

        # find non numeric values ----
        df.Rate = df.Rate.astype(str)
        df['alpha_test'] = df.Rate.apply(lambda x: re.findall('[aA-zZ]', x))
        df['alpha_test'] = df.alpha_test.apply(lambda x: len(x))
        non_num_mask = df.alpha_test > 0
        df = df[~non_num_mask].copy()
        df = df.loc[:, ['Date', 'Rate']]
        df.Rate = df.Rate.astype(float)

    else:
        df.rename(columns={'Date.1': 'Date',
                           'Rate.1': 'Rate'},
                  inplace=True)
        df.dropna(inplace=True)

        # find non numeric values ----
        df.Rate = df.Rate.astype(str)
        df['alpha_test'] = df.Rate.apply(
            lambda x: re.findall('[aA-zZ]', x))
        df['alpha_test'] = df.alpha_test.apply(lambda x: len(x))
        non_num_mask = df.alpha_test > 0
        df = df[~non_num_mask].copy()
        df = df.loc[:, ['Date','Rate']]
        df.Rate = df.Rate.astype(float)
    return df

def rate_separation():

    rate_list = []

    # treasury ----
    treasury_rates = read_spreadsheet(sheet='Treasury Rates')
    treasury_rates.dropna(inplace=True)
    rate_list.append(treasury_rates)

    # swap rates ----
    swap_rates = read_spreadsheet(sheet='SWAPS')
    swap_rates.dropna(inplace=True)
    rate_list.append(swap_rates)

    # other rates ----
    other_rates = read_spreadsheet(sheet='Other Rates', other_rates=True)
    other_rates.Date = other_rates.Date.astype(str).str[0:10]
    other_rates.Date = other_rates.Date.astype(object)
    prime_rates = other_rates.iloc[:, 0:2]
    cad_rates = other_rates.iloc[:, 3:5]

    # clean separate other rates ----
    prime_rates, cad_rates = other_rate_clean(prime_rates), \
                             other_rate_clean(cad_rates,  prime=False)
    rate_list.append(prime_rates)
    rate_list.append(cad_rates)

    return rate_list


# run from powershell ----
if __name__ == '__main__':

    try:
        rate_names = [ 'treasury', 'swaps', 'prime', 'cad' ]
        rate_list = rate_separation()
        rate_dict = dict(zip(rate_names, rate_list))

        # export to individual csv ----
        rate_dict[ 'treasury' ].to_csv(r'C:\Users\Noe_N\OneDrive\Market '
                                       r'Data\market_dashboard\market_data\Treasury'
                                       r'.csv', index=False)

        for name, rates in rate_dict.items():
            rates.to_csv(r'C:\Users\Noe_N\OneDrive\Market '
                         r'Data\market_dashboard\market_data\{}'
                         r'.csv'.format(name), index=False)

    except:
        print("There appears to be an error with the compilation.")
