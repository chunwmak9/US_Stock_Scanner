from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
import stock_algo as algo
from datetime import date
import datetime
import yahoo_fin.stock_info as stock_info
import time
import math



from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
import requests
import re
import pandas as pd
import numpy as np
import quandl


import ssl


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


class HKStock_Getter:
    def __init__(self):
        pass

    def get_codes(self)-> List[int]:
        #http://billylkc.com/2021/06/21/getting-hkex-data-with-quandl-in-python/
        

        regex = re.compile(r"\s*(\d{5})(.*)")  # Get 5 digit codes only
        #re_chinese = re.compile(r"(\d{5})")#Get HK stock Chinese Name


        url = "https://www.hkexnews.hk/sdw/search/stocklist_c.aspx?sortby=stockcode&shareholdingdate={}".format(
            datetime.today().strftime("%Y%m%d")
        ) # derive url, e.g. https://www.hkexnews.hk/sdw/search/stocklist_c.aspx?sortby=stockcode&shareholdingdate=20210621

        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        
        codes = []
        count = 0
        for s in soup.select("table.table > tbody > tr"):
            count+=1
            
            text = s.get_text().replace(" ", "").strip()  # Replace extra spaces
            matchResult = regex.search(text)
            
            if matchResult:
                code = int(matchResult.group(1).lstrip("0"))  # Convert to int, e.g. 00005 to 5

                if code <= 10000:  # main board only
                    codes.append((code,text.split()[1]))
      
        tickers = []
        for c in codes:
            c0 = c[0]#HK tickers code
            c1 = c[1]#HK tickers name
            if len(str(c0)) <4:
                c0 = "0"*(4-len(str(c0)))+str(c0)+".HK"
                tickers.append([c0 ,c1])
            else:
                c0 = str(c0)+".HK"
                tickers.append([c0,c1])
        return tickers 
        #All tickers are tested for availability with Yahoo Finance
        
class StockGetter(object):
    def __init__(self): #initial setup parameters here e.g year ,duration,number of data
        pass
    #You can input the start to end date of certain stock token to get the data from yahoo finance online
    def get_data(self,s,e,stock):
        self.start_date = s
        self.end_date = e
        self.token = stock #stock name
        self.data = yf.download(self.token,self.start_date,self.end_date)
        return self.data
    #You can input data as the data in y-axis e.g Open price of stock, methods => methods of plotting
    #functions set=> functions to process your data and plot out on graph ,key=>optional - for data df from online
    #The plot will be store on a parameters "plt" and WILL NOT be automatically plotted out
    
    def get_all_tokens(self):
        #Stock_data
        naq = stock_info.tickers_nasdaq()
        dow = stock_info.tickers_dow()
        sp500 = stock_info.tickers_sp500()
        other_stocks = stock_info.tickers_other()
        hkex_stocks = HKStock_Getter().get_codes()
        hkex_tickers = [hkex_stocks[i][0] for i in range(len(hkex_stocks))]
        #hkex_names= [hkex_stocks[i][1] for _ in range(len(hkex_stocks))]
        tokens = naq+dow+sp500+other_stocks+hkex_tickers # all stock data input
        return tokens

    def price_plot_data(self,data,methods,functions,key="Open"):
        global plt
        x = np.array([i for i in range(len(data))])
        # x_date = x #data[key].index 
        y = data[key]
        # print("Data:{}".format(len(data[key].index)))
        # print(len(y))
        plt.grid()
        plt.tight_layout(pad=3.0)
        for i in methods:
            if i == "line":
                plt.plot(x,y,color="green")
                if plt:
                    plt.ylabel("USD Price")
                    plt.xlabel("Date From {} to {}".format(self.start_date,self.end_date))
                    plt.title("{0} {1} Data Graph".format(self.token,key))
            elif i == "scatter":
                plt.scatter(x,y,color='magenta',marker='o')
                if plt:
                    plt.ylabel("USD Price")
                    plt.xlabel("Date From {} to {}".format(self.start_date,self.end_date))
                    plt.title("{0} {1} Data Graph".format(self.token,key))
            else:
                pass
        for f in functions:
            if f == "regression":
                reg = algo.ALGORITHMS()
                reg_func = reg.regression(x,y)
                #print(len(reg_func[0]))
                #print(len(reg_func[1]))
                plt.plot(reg_func[0],reg_func[1],color="blue")
                plt.annotate("b1(slope) = {}".format(reg_func[2]),(0,y.min()))
            elif f == "mean":
                pass
            elif f == "volatility":
                vol = algo.ALGORITHMS()
                vol_func = vol.volatility(x,y)
                plt.annotate("volatility = %s"%str(vol_func),(0,y.max()))
            elif f == "return_rate":
                ret = algo.ALGORITHMS()
                try:
                    y_open = data['Open']
                    y_close = data['Adj Close']
                except:
                    raise Exception("The data input does not contain keys 'Open' or 'Adj Close'.  ")
                ret_func = ret.return_rate(y_open,y_close) #f(open_price,close_price)
                #print(ret_func)
                #print(y_open['2021-09-13'])
                #print(y_close['2021-09-13'])
                
                plt.title("{} Daily Return Rate".format(self.token))
                plt.xlabel('Return Rate(%)')
                plt.ylabel('Frequency')
                ret_func_mean = ret_func.mean()
                hist = plt.hist(ret_func,bins=100)
                total = math.pow(1+(ret_func_mean/100),len(x))*100 - 100 #total P&L
                #total = ret_func.sum() /100
                plt.annotate("Mean Return Rate = {}%".format(str(ret_func_mean)),(ret_func_mean,hist[0].max()))
                plt.annotate("Average total P&L between {} and {} = {}%".format(str(self.start_date),str(self.end_date),str(round(total,6))),(ret_func_mean,hist[0].mean()))
                plt.axvline(ret_func_mean,color="magenta")
                plt.hist(ret_func,bins=100)
            elif f == "sentiment score":
                import sentiments
                s = sentiments.sentiments()
                sentiments_table = s.get_sentiment_score([self.token]) #input:[token_code]  ,output:return [ df1 ]
                try:
                    print(sentiments_table)
                    dates = sentiments_table[0]['date']
                    compounds = sentiments_table[0]['compound']
                    #if len(dates)>400:
                    #    dates = sentiments_table[0]['date'][:400]
                    #    compounds = sentiments_table[0]['compound'][:400]
                    #d = [i if int(i.split("-")[0])>=int(self.start_date.split("-")[0]) else 0 for i in dates ]
                    #print(self.start_date.split("-")[0])
                    #plt.bar(d,[compounds[j] for j in range(len(d))])
                    plt.bar(dates,compounds,width=0.5)
                    plt.title("{} News Analysis".format(self.token))
                    plt.ylabel("S Scores")
                    plt.xlabel("Dates")
                    
                    
                except:
                    pass


        
            
                
if __name__ == "__main__":
    pass






    """
    i = 0

    sg = sdata.StockGetter()
    today = date.today()
    now = today.strftime('%Y-%m-%d')
    tickers =  stock_info.get_day_gainers()['Symbol']    #stock_info.tickers_other()
    #stock_info: tickers_dow(),tickers_nasdaq(),tickers_other(),tickers_sp500()
    #Daily_stock: get_day_gainers(),get_day_most_active(),get_day_losers(),get_top_crypto()
    print(tickers)
    np.random.shuffle(tickers)
    
    while i < len(tickers): 
        try:
            data = sg.get_data('2020-9-1',now,tickers[i]).keys()
            data = sg.get_data('2020-9-1',now,tickers[i])
            methods= ['scatter','line']
            functions = ['regression','mean','volatility']
            plt.figure(figsize=(15,7))
            plt.subplot(1,2,1)
            sg.price_plot_data(data,methods,functions,'Open')
            plt.subplot(1,2,2)
            sg.price_plot_data(data,methods,functions,'Volume')
            plt.show()
            
        except KeyboardInterrupt:
            exit()

    """

    """
    while True:
        sg = StockGetter()
        today = date.today()
        now = today.strftime('%Y-%m-%d')
        print(now)
        print(sg.get_data('2021-1-12',now,'NNDM').keys())
        token = str(input("Input the Stock Code: ")) #e.g NNDM 
        try:
            key = str(input("Input the type of data(NA=>Default Key): ")) #e.g Open
        except ValueError:
            key = "Open"
        data = sg.get_data('2020-1-12',now,token)
        print(data)
        methods= ['scatter','line']
        functions = ['regression','mean','volatility']
        sg.price_plot_data(data,methods,functions,key)
        """

#Reference: https://algotrading101.com/learn/yahoo-finance-api-guide/