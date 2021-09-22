import stock_algo as algo
import stock_data as sdata
from datetime import date
import yahoo_fin.stock_info as stock_info
import numpy as np
from matplotlib import pyplot as plt

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class user_interface(object):
    def __init__(self,plt):
        self.window = tk.Tk()
        self.plt = plt
        self.fig = FigureCanvasTkAgg(self.plt, self.window)
        return self.window.mainloop()






if __name__ == "__main__":
    #app = user_interface()
    i = 0

    sg = sdata.StockGetter()
    today = date.today()
    now = today.strftime('%Y-%m-%d')
    #tickers = stock_info.tickers_other() #stock_info.get_day_gainers()['Symbol']    
    #stock_info: tickers_dow(),tickers_nasdaq(),tickers_other(),tickers_sp500()
    #Daily_stock: get_day_gainers(),get_day_most_active(),get_day_losers(),get_top_crypto()
    #tickers = stock_info.get_day_losers()['Symbol']
    tickers = stock_info.tickers_nasdaq()
    #print(tickers)
    np.random.shuffle(tickers)
    #print(sg.get_data('2020-9-1',now,tickers[i]).keys())
    #print(stock_info.get_balance_sheet("NNDM"))
    print(len(tickers))
    #tickers = ["DGLY"]
    while i < len(tickers): 
        try:
            data = sg.get_data('2021-1-1',now,tickers[i])
            #Keys: ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
            method1= ['scatter','line']
            function1 = ['regression','mean','volatility']
            method2 = []
            function2 = ['return_rate']
            method3 = []
            function3 = ['sentiment score']


            plt.figure(figsize=(15,7))
            plt.subplot(1,2,1)
            sg.price_plot_data(data,method1,function1,'Open')
            plt.subplot(1,2,2)
            sg.price_plot_data(data,method2,function2)
            plt.figure(figsize=(15,7))
            sg.price_plot_data(data,method3,function3)
            plt.grid()

            plt.show()
            
            i+=1

        except KeyboardInterrupt:
            exit()
        
#Reference: https://algotrading101.com/learn/yahoo-finance-api-guide/
"""
stock_info has the following methods:

get_analysts_info()
get_balance_sheet()
get_cash_flow()
get_data()
get_day_gainers()
get_day_losers()
get_day_most_active()
get_holders()
get_income_statement()
get_live_price()
get_quote_table()
get_top_crypto()
get_stats()
get_stats_valuation()
tickers_dow()
tickers_nasdaq()
tickers_other()
tickers_sp500()

And options has:

get_calls()
get_expiration_dates()
get_options_chain()
get_puts()



"""