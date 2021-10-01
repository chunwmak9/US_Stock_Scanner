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


class user_interface(object):
    def __init__(self,stock_data):
        self.stock_data = stock_data
        return self.GUI()
        
    def GUI(self):
        self.window = Tk()
        self.window.title("Stock Screener")
        self.window.geometry("600x200+500+200")
        def scrollbar(kw):
            try:
                self.window.destroy()
                self.window = Tk()
                self.window.title("Stock Screener")
                self.window.geometry("1400x600+500+200")
                self.scrollbar = Scrollbar(self.window)
                self.scrollbar.pack(side=RIGHT,fill=Y)
                self.text = StringVar()
                self.news = Label(self.window,textvariable=self.text)
                def onselect(evt):
                    w =  evt.widget
                    index = int(w.curselection()[0])
                    value = w.get(index)
                    sent = se.sentiments()
                    news = sent.get_news([value])
                    news_lines =""
                    if len(news[value])>15:
                        news[value] = news[value][:16]
                    for l in news[value]:
                        #news_lines+= " ".join(l[0:])  +"\n"
                        # if len(l[3])>30:
                        #     while True:
                        #         if l[3].find(" ") >= 30:
                        #             l[3] = l[3][:l[3].find(" ")+1]+l[3][l[3].find(" "):].replace(" ","\n",1)
                        #             break
                                

                        AL = " ".join(l[0:])
                        
                        news_lines+= AL
                        news_lines+="\n"+"\n"

                    self.text.set("NEWS \n \n \n"+news_lines)

                self.gui_list = Listbox(self.window,yscrollcommand = self.scrollbar.set)
                self.gui_list.bind('<<ListboxSelect>>', onselect)
                selected_stock_data = [d for d in self.stock_data if kw.upper() in d ]
                for token in selected_stock_data:
                    self.gui_list.insert(END,str(token))
                def select_item():
                    for s in self.gui_list.curselection():
                        stock = self.gui_list.get(s)
                        print("You selected {}".format(self.gui_list.get(s)))
                        #Selected data
                        sg = sdata.StockGetter()
                        data = sg.get_data('2020-1-1',now,self.gui_list.get(s))
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
                        self.window.destroy()
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


                
                #Enter button
                self.btn1 = Button(self.window,text = "Select",command=select_item)
                
                self.btn1.pack(side="bottom")
                self.gui_list.pack(side=LEFT,fill=BOTH)
                self.news.pack(side="top",fill=BOTH)
                #self.btn1.grid(row=1,column=1)
                #self.gui_list.grid(row=0,column=0)
                #self.news.grid(row=0,column=1)

                self.scrollbar.config(command=lambda:self.gui_list.size(2))
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
    tokens = naq+dow+sp500+other_stocks # all stock data input
    app = user_interface(tokens) #input stock data


    
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