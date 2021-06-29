import pandas as pd
from td.client import TDClient
import requests
import json
from datetime import date
import time
import urllib
import requests
from splinter import Browser
from coinbase.wallet.client import Client
from config import client_id, username, password, cb_key, cb_secret, act_num
from config import question1, answer1, question2, answer2, question3, answer3, question4, answer4


class collection():

    def td_ameritrade(self):

        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)
        method = 'GET'
        url = 'https://auth.tdameritrade.com/auth?'
        client_code = client_id + '@AMER.OAUTHAP'
        payload_auth = {'response_type': 'code', 'redirect_uri': 'http://127.0.0.1',
                        'client_id': client_code}

        built_url = requests.Request(method, url, params=payload_auth).prepare()

        my_url = built_url.url
        browser.visit(my_url)

        # Fill Out the Form
        payload_fill = {'username': username, 'password': password}
        browser.find_by_id('username0').first.fill(payload_fill['username'])
        browser.find_by_id('password1').first.fill(payload_fill['password'])
        browser.find_by_id('accept').first.click()
        time.sleep(1)

        # Get the Text Message Box
        browser.find_by_text('Can\'t get the text message?').first.click()

        # Get the Answer Box
        browser.find_by_value("Answer a security question").first.click()

        # Answer the Security Questions.
        if browser.is_text_present(question1):
            browser.find_by_id('secretquestion0').first.fill(answer1)
        elif browser.is_text_present(question2):
            browser.find_by_id('secretquestion0').first.fill(answer2)
        elif browser.is_text_present(question3):
            browser.find_by_id('secretquestion0').first.fill(answer3)
        elif browser.is_text_present(question4):
            browser.find_by_id('secretquestion0').first.fill(answer4)
        else:
            raise ValueError('Security question and answer not found in config file.')

        # Submit results
        browser.find_by_id('accept').first.click()

        # Trust this device
        browser.find_by_xpath('/html/body/form/main/fieldset/div/div[1]/label').first.click()
        browser.find_by_id('accept').first.click()

        # Sleep and click Accept Terms.
        time.sleep(1)
        browser.find_by_id('accept').first.click()
        time.sleep(1)

        new_url = browser.url
        parse_url = urllib.parse.unquote(new_url.split('code=')[1])
        browser.quit()

        # Define the endpoint
        url = r"https://api.tdameritrade.com/v1/oauth2/token"

        # define the headers
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # define the payload
        payload = {'grant_type': 'authorization_code',
                   'access_type': 'offline',
                   'code': parse_url,
                   'client_id': client_id,
                   'redirect_uri': 'http://127.0.0.1'}

        # post the data to get the token
        authReply = requests.post(r'https://api.tdameritrade.com/v1/oauth2/token',
                                  headers=headers, data=payload)

        # convert it to a dictionary
        decoded_content = authReply.json()

        # grab the access_token
        access_token = decoded_content['access_token']
        headers = {'fields': 'fields=positions',
                   'Authorization': "Bearer {}".format(access_token)}

        # define an endpoint with a stock of your choice, MUST BE UPPER
        endpoint = r"https://api.tdameritrade.com/v1/accounts/{}".format(act_num)

        # define the payload
        # payload = {'apikey': api_key}

        # make a request
        content = requests.get(url=endpoint, headers=headers)

        # convert it dictionary object
        self.data = content.json()

    def td_data(self):
        cashAvail = self.data['securitiesAccount']['initialBalances']['cashAvailableForTrading']
        acctValue = self.data['securitiesAccount']['initialBalances']['accountValue']
        assetValue = self.data['securitiesAccount']['initialBalances']['longStockValue']

        tdValues = {'Date': date.today(),
                    'TD_Cash': cashAvail,
                    'TD_Account_Value': acctValue,
                    'TD_Asset_Value': assetValue}

        self.tdValues = pd.DataFrame.from_dict(tdValues, orient='index').T
        self.tdValues.set_index('Date', inplace=True)

        return self.tdValues

    def coinbase(self):
        client = Client(cb_key, cb_secret)
        accounts = client.get_accounts()

        message = {}
        total = 0

        for wallet in accounts.data:
            message.update({str(wallet['name']): float(wallet['native_balance']['amount'])})
            total += float(wallet['native_balance']['amount'])
        message.update({'Total Balance: ': total})

        cb_df = pd.DataFrame.from_dict(message, orient='index', columns=['CB_Wallets'])
        self.cb_df = cb_df.loc[(cb_df != 0).any(axis=1)]

        return self.cb_df

    def merge(self):
        cb_total = self.cb_df.CB_Wallets[-1]
        print(cb_total)
        self.tdValues.insert(3, column='CB_Total', value=cb_total)

        return self.tdValues
