from collection import collection

print('Fetching TD Ameritrade Account Data. . .')
data = collection()
td = data.td_ameritrade()
td_data = data.td_data()

print('Fetching Coinbase Account Data. . .')
cb_data = data.coinbase()

print('Combining. . .')
assets = data.merge()

print('----- Total Value of All Assets -----', '\n')
print(assets['TD_Account_Value'] + assets['CB_Total'])