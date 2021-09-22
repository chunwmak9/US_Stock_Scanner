import numpy as np


#std,mean,range(max,min spread)

#Volatility

class ALGORITHMS(object):
    def volatility(self,x,y):
        #Variance =>e.g y: price data,x:samples
        a = ((x-x.mean())**2)
        b = len(x)-1
        variance = a.sum()/b
        volatility = variance 
        #Dailiy to annualized volatility = variance * np.sqrt(252)
        return volatility

    def regression(self,x,y): #y here is the data set
        try:
            y = np.array(y)
            x = np.array(x)
        except:
            pass
        n = len(x)
        b1_u = np.sum(x*y)-((np.sum(x)*np.sum(y))/n)
        b1_d = np.sum(x**2) - ((np.sum(x)**2)/n)
        b1 = b1_u/b1_d
        b0 = np.mean(y) - b1*(np.mean(x))
        reg_y = b0+b1*x
        reg_x = x
        slope = b1
        reg_data=[reg_x,reg_y,slope] 
        return reg_data
    def return_rate(self,open_price,close_price):
        return_rate_matrix = (close_price-open_price)/open_price
        return_rate_matrix *= 100 #return the return rate in percentage 
        return return_rate_matrix




if __name__ == "__main__":
    algo = ALGORITHMS()
    print(algo.regression(np.arange(0,100),np.arange(0,100)))

