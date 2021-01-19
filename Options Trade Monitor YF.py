#Options trade monitor for Yahoo Finance
#Duncan McDonld
#no copyright implied
#
#
#Yahoo Finance option tracking is not the best, so if the results
#with this script seem erratic, check Yahoo Finance directly and see if the data is there
#
# You can test this script with the following OCC codes:
#(Sell) AAPL210416P100
#(Buy) AAPL210416P95
#(Sell) AAPL210416C155
#(Buy) AAPL210416C160
#
# You'll need to install PySimpleGUI
# pip install PySimpleGUI
#
#Feedback or advice?
#dmcdonald999@gmail.com
#Reddit: u/Duncan999
#

import PySimpleGUI as sg
import yfinance as yf
import pandas as pd
import re

#tuple indexes
bid = 1
ask = 2
mid = 3
last = 4
radio = 5

counter = 0
loop_running = False

#number of rows (legs) in table excluding summary row
rows = 4

#setup GUI
sg.theme('SandyBeach')
 
layout = [ 
    [sg.Text('Enter legs in OCC format, no spaces')], 
    [sg.Text('Leg 1', size =(5, 1)), sg.InputText(size=(20, 1),key='LEG_1'),sg.Text('Bid', size =(3, 1)), sg.Text(size=(7,1),
        background_color='#e6d4a8', relief='sunken', border_width=1, key=(bid,0)),sg.Text('Ask', size =(3, 1)), sg.Text(size=(7,1),
        background_color='#e6d4a8', relief='sunken', border_width=1, key=(ask,0)),sg.Text('Mid', size =(3, 1)), sg.Text(size=(7,1),
        background_color='#e6d4a8', relief='sunken', border_width=1, key=(mid,0)), sg.Text('Last', size =(3, 1)), sg.Text(size=(7,1),
        background_color='#e6d4a8', relief='sunken', border_width=1, key=(last,0))],
    
    [sg.T("         "), sg.Radio('Sell', "RADIO1", default=True, key=(radio,0)), sg.Radio('Buy',  "RADIO1", default=False)],
    [sg.Text('Leg 2', size =(5, 1)), sg.InputText(size=(20, 1),key='LEG_2'),sg.Text('Bid', size =(3, 1)), sg.Text(size=(7,1),
        background_color='#e6d4a8', relief='sunken', border_width=1, key=(bid,1)),sg.Text('Ask', size =(3, 1)), sg.Text(size=(7,1),
        background_color='#e6d4a8', relief='sunken', border_width=1, key=(ask,1)),sg.Text('Mid', size =(3, 1)), sg.Text(size=(7,1),
        background_color='#e6d4a8', relief='sunken', border_width=1, key=(mid,1)),sg.Text('Last', size =(3, 1)),sg.Text(size=(7,1),
        background_color='#e6d4a8', relief='sunken', border_width=1, key=(last,1))], 

    [sg.T("         "), sg.Radio('Sell', "RADIO2", default=True, key=(radio,1)), sg.Radio('Buy', "RADIO2", default=False)],
    [sg.Text('Leg 3', size =(5, 1)), sg.InputText(size=(20, 1),key='LEG_3'),sg.Text('Bid', size =(3, 1)), sg.Text(size=(7,1),
        background_color='#e6d4a8', relief='sunken', border_width=1, key=(bid,2)),sg.Text('Ask', size =(3, 1)), sg.Text(size=(7,1),
        background_color='#e6d4a8', relief='sunken', border_width=1, key=(ask,2)),sg.Text('Mid', size =(3, 1)), sg.Text(size=(7,1),
        background_color='#e6d4a8', relief='sunken', border_width=1, key=(mid,2)),sg.Text('Last', size =(3, 1)),sg.Text(size=(7,1),
        background_color='#e6d4a8', relief='sunken', border_width=1, key=(last,2))], 

    [sg.T("         "), sg.Radio('Sell', "RADIO3", default=True, key=(radio,2)), sg.Radio('Buy',  "RADIO3", default=False)],
    [sg.Text('Leg 4', size =(5, 1)), sg.InputText(size=(20, 1),key='LEG_4'),sg.Text('Bid', size =(3, 1)), sg.Text(size=(7,1),
        background_color='#e6d4a8', relief='sunken', border_width=1, key=(bid,3)),sg.Text('Ask', size =(3, 1)), sg.Text(size=(7,1),
        background_color='#e6d4a8', relief='sunken', border_width=1, key=(ask,3)),sg.Text('Mid', size =(3, 1)), sg.Text(size=(7,1),
        background_color='#e6d4a8', relief='sunken', border_width=1, key=(mid,3)),sg.Text('Last', size =(3, 1)),sg.Text(size=(7,1),
        background_color='#e6d4a8', relief='sunken', border_width=1, key=(last,3))], 

    [sg.T("         "), sg.Radio('Sell', "RADIO4", default=True, key=(radio,3)), sg.Radio('Buy',  "RADIO4", default=False)],
    [sg.Text('')],
    [sg.Text('Net Trade        ', font=1), sg.Text('Bid', size =(3, 1), font=1), sg.Text(size=(7,1), background_color='#e6d4a8', relief='sunken', text_color='black', border_width=1, key=(bid,4)),
    sg.Text('Ask', size =(3, 1), font=1), sg.Text(size=(7,1), background_color='#e6d4a8', relief='sunken', text_color='black', border_width=1, key=(ask,4)),
    sg.Text('Mid', size =(3, 1), font=1), sg.Text(size=(7,1), background_color='#e6d4a8', relief='sunken', text_color='black', border_width=1, key=(mid,4)),
    sg.Text('Last', size =(4, 1), font=1), sg.Text(size=(7,1), background_color='#e6d4a8', relief='sunken', text_color='black', border_width=1, key=(last,4))], 
    [sg.Text('')],
    [sg.Text('')],
    [sg.Button('Start/Stop', size=(10, 1)), sg.Exit('Exit', size=(5, 1))]
]
window = sg.Window('Options Trade Monitor For Yahoo Finance', layout) 

# The Event Loop
while True:
    event, values = window.read(timeout=10)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Start/Stop':
        loop_running = not loop_running
    if loop_running:
        counter = counter + 1
        #uncomment the following if you want to see how fast the loop is running
        #print(counter)
        
        #the calculation loop
        #initialize summing variables
        sum_bid = 0
        sum_ask = 0
        sum_last = 0
        sum_mid = 0
        #count the number of non-blank legs
        non_blank = 0
        for x in range(rows):
            if ('LEG_' + str(x+1)) != '':
                non_blank = non_blank + 1
                
        #repeat this block for each leg
        #for loop start
        for x in range(non_blank):
            text_input = values['LEG_' + str(x+1)]
            match = re.match(r"([a-z]+)([0-9]+)", text_input, re.I) #gets first two tokens
            if match:
                #extract the ticker
                ticker = match.group(1)
                #extract the date and insert hyphens in the extracted expiration
                a = match.group(2)
                b = '20' + a
                expiration = ('-'.join([b[:4], b[4:6], b[6:]]))
                #extract the call/put and strike price
                b = text_input.replace(ticker, '')
                c = b.replace(a, '')
                match = re.match(r"([a-z]+)([0-9]+)", c, re.I) #gets next two tokens
                #extract the call/put
                call_put = match.group(1) #ignore warning  Item "None" of "Optional[Match[Any]]" has no attribute "group"
                #extract the strike price
                strike_price = match.group(2) #ignore warning  Item "None" of "Optional[Match[Any]]" has no attribute "group"

                #download the option chain for ticker and date
                #first set the display so it won't abbreviate the table
                pd.set_option('display.max_rows', None)
                pd.set_option('display.max_columns', None)
                pd.set_option('display.width', None)
                pd.set_option('display.max_colwidth', None)
                tcker = yf.Ticker(ticker)
                opt = tcker.option_chain(date=expiration)
                if call_put == 'C':
                    data = opt.calls
                else:
                    data = opt.puts
                    
                #extract the bid/ask/last for the price and call/put
                bids = data.loc[data['strike'] == int(strike_price), 'bid'].item()
                asks = data.loc[data['strike'] == int(strike_price), 'ask'].item()
                lasts = data.loc[data['strike'] == int(strike_price), 'lastPrice'].item()
                #calculate mid price
                mids = bids + (asks - bids)/2
                
                #calculate the sums of the legs; sell is positive, buy is negative
                if(values[(radio,x)]) == True:
                    sum_bid = sum_bid + bids
                    sum_ask = sum_ask + asks
                    sum_last = sum_last + lasts
                    sum_mid = sum_mid + mids
                else:
                    sum_bid = sum_bid - bids
                    sum_ask = sum_ask - asks
                    sum_last = sum_last - lasts
                    sum_mid = sum_mid - mids
                    
                #display data
                window[(bid,x)].update(bids)
                window[(ask,x)].update(asks)
                window[(mid,x)].update('{:03.2f}'.format(mids))
                window[(last,x)].update(lasts)
        #for loop end
        if x == 3: #after last leg, calculate sums
            window[(bid,4)].update('{:03.2f}'.format(sum_bid))
            window[(ask,4)].update('{:03.2f}'.format(sum_ask))
            window[(last,4)].update('{:03.2f}'.format(sum_last))
            window[(mid,4)].update('{:03.2f}'.format(sum_mid))
        #main loop end
window.close()
        

#test OCC's
#TSLA201218C139
#tsla201218p665

#option_chain for ticker
#calls/puts for ticker and date
    #contractSymbol
    #lastTradeDate
    #strike
    #lastPrice
    #bid
    #ask
    #change
    #percentChange
    #volume
    #openInterest
    #impliedVolatility
    #inTheMoney
    #contractSize
    #currency

