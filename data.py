import os
import re
import sys
import pandas as pd
import json
import requests
from datetime import datetime

YEAR = datetime.now().year

TICKERS_FILE = "tickers.txt"

def getDataframe():
    apiKey = getAPIKey()
    tickers = getTickers()

    df = getData(apiKey, tickers)
    df['date'] = pd.to_datetime(df['date'])
    df.iloc[:, 2:] = df.iloc[:, 2:].apply(pd.to_numeric)

    return df


def getData(apiKey, tickers):
    df = pd.DataFrame()

    for ticker in tickers:
        jsonData = getRatios(ticker, apiKey)

        temp = pd.json_normalize(jsonData)
        temp = temp.drop('period', axis=1)

        df = pd.concat([df, temp], axis=0)

    return df


def getAPIKey():
    apiKey = ""

    # get text from first line of config.txt
    with open('config.txt', 'r') as f:
        apiKey = f.readline()

    return apiKey


def getTickers():
    tickers = []

    # get tickers from tickers.txt
    with open(TICKERS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            line = line.upper()
            tickers.append(line)

    return tickers

def getRatios(ticker, apiKey):
    url = "https://financialmodelingprep.com/api/v3/ratios/{}?limit=40&apikey={}".format(ticker, apiKey)

    print("Url: {}".format(url))

    # check if folder ratios exists
    if not os.path.exists('ratios'):
        os.makedirs('ratios')

    PATH = 'ratios/{}_{}.json'.format(ticker, YEAR-1)

    if (os.path.exists(PATH)):
        with open(PATH, 'r') as f:
            print("Found ratios for {} in file".format(ticker))

            data = json.load(f)
    else:
        response = requests.get(url)
        data = response.json()

        if not data or 'Error Message' in data:
            sys.exit("Error getting ratios for {}".format(ticker))

        with open(PATH, 'w') as f:
            print("Saving ratios for {} to file".format(ticker))
            json.dump(data, f)

    return data
