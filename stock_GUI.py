import stock_algo as algo
import stock_data as sdata
from datetime import date
import yahoo_fin.stock_info as stock_info
import numpy as np
from matplotlib import pyplot as plt

from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sentiments as se

import yfinance as yf
from keywords_trend import keywords

from stock_data import HKStock_Getter



class user_interface(object):
    def __init__(self,stock_data):
        self.stock_data = stock_data
        self.news_lines = ""
        self.index = -1
        self.value = -1
        return self.GUI()
        
    def GUI(self):
        self.window = Tk()
        self.window.title("Stock Screener")
        self.window.geometry("600x200+500+200")
        
        def scrollbar(kw):
            try:
                #self.window.destroy()
                self.window = Tk()
                self.window.title("Stock Screener")
                self.window.geometry("1400x600+500+200")
                self.scrollbar = Scrollbar(self.window)
                self.scrollbar.pack(side=RIGHT,fill=Y)
                self.text = StringVar(self.window)
                self.news = Text(self.window,height=300, width=500)
                
                #Stock Option Menu                
                self.selected_option = StringVar()
                self.selected_option.set("NEWS")
                options_menu = ["NEWS","Information","Balance Sheet"]

                def option_check():
                    #Option menu selection
                    if self.selected_option.get()== "NEWS":
                        self.text.set("NEWS \n \n \n"+self.news_lines)
                    elif self.selected_option.get()== "Balance Sheet":
                        self.text.set(get_stock_info("balance sheet"))
                    else:
                        self.text.set(get_stock_info("other"))
                    self.news.delete(1.0, END)
                    self.news.insert(END,self.text.get())
                    
                def options_select(evt):
                    option_check()
                
                
                def onselect(evt):
                    w =  evt.widget
                    if self.index== -1:
                        self.index = int(w.curselection()[0])
                    self.value = w.get(self.index)
                    sent = se.sentiments()
                    news = sent.get_news([self.value])
                    self.news_lines  =""
                    if len(news[self.value])>15:
                        news[self.value] = news[self.value][:16]
                    for l in news[self.value]:
                        #news_lines+= " ".join(l[0:])  +"\n"
                        # if len(l[3])>30:
                        #     while True:
                        #         if l[3].find(" ") >= 30:
                        #             l[3] = l[3][:l[3].find(" ")+1]+l[3][l[3].find(" "):].replace(" ","\n",1)
                        #             break
                                

                        AL = " ".join(l[0:])
                        
                        self.news_lines += AL
                        self.news_lines+="\n"+"\n"
                    #Select Checking
                    option_check()
                   
                
                self.gui_list = Listbox(self.window,yscrollcommand = self.scrollbar.set)
                self.gui_list.bind('<<ListboxSelect>>', onselect)
                selected_stock_data = [d for d in self.stock_data if kw.upper() in d ]
                for token in selected_stock_data:
                    self.gui_list.insert(END,str(token))

                def get_stock_info(info):
                    stock = ""

                    for s in self.gui_list.curselection():
                        stock = self.gui_list.get(s)
                    if stock == "":
                        return ""
                    if info == "balance sheet":
                        return str(yf.Ticker(stock).balance_sheet)
                    elif info == "other":
                        INFO = ""
                        yinfo = yf.Ticker(stock).info
                        for k in yinfo.keys():
                            INFO+=str(k)+" : "+str(yinfo[k])+"\n"

                        return str(yf.Ticker(stock).calendar)+"\n" +str(yf.Ticker(stock).financials)+"\n" +INFO+"\n" +str(yf.Ticker(stock).earnings)+"\n"+"\n" +str(yf.Ticker(stock).earnings)+"\n Holders of Stock"+str(yf.Ticker(stock).major_holders)+"\n"+str(yf.Ticker(stock).institutional_holders)

                        


                def select_item():
                    for s in self.gui_list.curselection():
                        stock = self.gui_list.get(s)
                        print("You selected {}".format(self.gui_list.get(s)))
                        #Selected data
                        trend = keywords.Trends()

                        sg = sdata.StockGetter()
                        start_date = '2021-2-8' #trend.get_start_date(stock)  #'2020-1-1'
                        data = sg.get_data(start_date,now,self.gui_list.get(s))
                        #Keys: ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
                        method1= ['scatter','line']
                        function1 = ['regression','mean','volatility']
                        method2 = []
                        function2 = ['return_rate']
                        method3 = []
                        function3 = ['sentiment score']

                        plt.figure(figsize=(15,7))
                        # plt.tight_layout(pad=3.0)
                        # plt.grid()
                        
                        plt.subplot(2,2,1)
                        sg.price_plot_data(data,method1,function1,'Open')
                        plt.subplot(2,2,2)
                        sg.price_plot_data(data,method2,function2)
                        #plt.figure(figsize=(15,7))
                        plt.subplot(2,2,3)
                        sg.price_plot_data(data,method3,function3)
                        plt.subplot(2,2,4)
                        
                        trend_kw = "{} stock".format(stock)
                        sug_kws = trend.trends.suggestions(trend_kw)
                        if len(sug_kws)>=1:
                            trend_kw = sug_kws[0]["title"]
                        trend.search(trend_kw,date = start_date+" "+now,plot=True)
                        
                        #self.window.destroy()

                        
                        # def pop_up_news(stock):
                        #     news_win = Tk()
                        #     news_win.geometry("1000x600+600+600")
                            
                        #     news_win.title("News Window")
                        #     sent = se.sentiments()
                        #     news = sent.get_news([stock])
                        #     news_lines =""
                            
                        #     scrollbar_y = Scrollbar(news_win,orient="vertical")
                        #     news_text = Text(news_win,width=15,height=15,wrap=None,yscrollcommand=scrollbar_y.set)
                        #     news_text.insert(END,stock+" NEWS \n \n")
                        #     for l in news[stock]:
                        #         #news_lines+= " ".join(l[0:])  +"\n"
                        #         news_lines= " ".join(l[0:]) +"\n"
                        #         news_text.insert(END,news_lines)
                        #     print(news)
                        #     scrollbar_y.pack(side=RIGHT,fill=Y)
                        #     news_text.pack(side=TOP, fill=X)
                        #     news_win.mainloop()
                        #     news_win.destroy()
                        #pop_up_news(stock)
                        
                        plt.show()
                self.opt = OptionMenu(self.window, self.selected_option,*options_menu,command=options_select)

                
                #Enter button
                self.btn1 = Button(self.window,text = "Select",command=select_item)
                


                
                self.btn1.pack(in_=self.window,side="bottom")
                #self.btn3.pack(in_=self.window,side= "left")
                self.gui_list.pack(side=LEFT,fill=BOTH)
                self.opt.pack(side="bottom",fill=X)
                self.news.pack(side="top",fill=Y)
                #self.btn1.grid(row=1,column=1)
                #self.gui_list.grid(row=0,column=0)
                #self.news.grid(row=0,column=1)
                
                self.scrollbar.config(command=lambda:self.gui_list.size(2))
                self.window.mainloop()
            except:
                raise Exception("Please Enter a valid value again.")

        def get_search_input():
            kw = self.text1.get("1.0",END)#keywords from search
            return kw.split()[0]

        #The search text box
        self.label1 = Label(self.window,text="Stock Screen")
        self.text1  = Text(self.window,height=5,width=20)
        self.label1.config(font=("Courier",14))
        self.btn2 = Button(self.window,text="Search",command=lambda:scrollbar(get_search_input()))
        

        self.label1.pack()
        self.text1.pack()
        self.btn2.pack()
        
        
        self.window.mainloop()
    
    





if __name__ == "__main__":

    sg = sdata.StockGetter()
    now = date.today().strftime('%Y-%m-%d')
    #Stock_data
    naq = stock_info.tickers_nasdaq()
    dow = stock_info.tickers_dow()
    sp500 = stock_info.tickers_sp500()
    other_stocks = stock_info.tickers_other()
    hkex_stocks = HKStock_Getter().get_codes()
    hkex_tickers = [hkex_stocks[i][0] for i in range(len(hkex_stocks))]
    #hkex_names= [hkex_stocks[i][1] for _ in range(len(hkex_stocks))]
    tokens = naq+dow+sp500+other_stocks+hkex_tickers # all stock data input
    app = user_interface(tokens) #input stock data

    #print(easyquotation.use("hkquote"))
    
    """
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
        """
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