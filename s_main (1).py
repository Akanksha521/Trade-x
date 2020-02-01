import matlab.engine
import time
import hinder_csv as hc
import numpy as np 
import math
import matplotlib.pyplot as plt

start_time = time.time()


last_three =[]
pred_arr = []
act_arr=[]

def matlab_stuff(path):
    global last_three
    global pred_arr
    [predicted,last_three] = eng.prediction_gauss_3(path,nargout = 2)
    pred_arr.append(float(str(predicted)))
    


def win_check(second_last,third_last,current,pred):    up_win =30#abs(current-third_last)/3
    down_win = 30#abs(current-third_last)/3
    if(pred<=third_last+up_win and pred>=third_last-down_win):
        
        return True
        
        
    
        
def long_or_short(predicted,current,win_check_outp):
    if predicted >= current :
        lis = long_call(win_check_outp)
        return lis
    elif predicted < current :
        lis = short_call(win_check_outp)
        return lis


def long_call(win_check_outp):
   if win_check_outp == True:# or win_check_outp =='above':
        long = True
        short = False
        return [long,short]
    else:
        long = False
        short = False
        return [long,short]


        
def short_call(win_check_outp):
      
    if win_check_outp == True:# or win_check_outp =='below':
        long = False
        short = True
        return [long,short]
    else:
        long = False
        short = False
        return [long,short]


def trade(long,short):     if long:
        return(1)
    elif short:
        #print("sell") #return sell to make an api call
        return(0)
    elif long == False and short == False:
        #print("not trading")
        return(2)

    
def actual_money(invested,actual):
    global ini
    
    tr = trade(long,short)
    #actual = (hc.pick_data()[0])
    act_arr.append(float(str(actual)))
    if(tr == 1):
        worth = actual - invested
        return(worth)
    elif(tr == 0):
        return(0)
    elif(tr==2):
        return(0)
    
def virtual_money(invested,actual):
    act_arr.append(float(str(actual)))
    worth = actual - invested
    return(worth)

    
total = 0
day=[]
l_long = 0
l_short = 0
l_not = 0
axis=[]
each=[]
n=10
do = 0
for i in range(1,66):
    if(i%13==1 or i%13==2 or i%13==3 ):
        print("did not trade - "+ str(i))
        hc.pick_data()
        n_array=[]

    else:
        if(do<2):
            #print(do)
            print("real")
            matlab_stuff(r"C:\Users\Akanksha\Desktop\time series\BAJFINANCE_merger_2018.txt")
            pred = pred_arr[len(pred_arr)-1]# is the predicted value
            #print(pred)

            current = float(str(last_three[2][0]))

            third_last = float(str(last_three[0][0]))
            second_last = float(str(last_three[1][0]))
            win_check_outp = win_check(second_last,third_last,current,pred)
            lis = long_or_short(pred,current,win_check_outp)
            long = lis[0]
            short = lis[1]
            [next_val,date]=hc.pick_data()
            total = actual_money(current,next_val)
            axis.append(i)
            if long == True:
                l_long = l_long + 1
            if short == True:
                l_short = l_short + 1
            
            if(n<=0):
                do = do + 1
            else:
                do = 0
            #print(total)
        else:
            print("virtual")
            matlab_stuff(r"C:\Users\Akanksha\Desktop\time series\BAJFINANCE_merger_2018.txt")
            pred = pred_arr[len(pred_arr)-1]# is the predicted value
            #print(pred)

            current = float(str(last_three[2][0]))

            third_last = float(str(last_three[0][0]))
            second_last = float(str(last_three[1][0]))
            win_check_outp = win_check(second_last,third_last,current,pred)

            lis = long_or_short(pred,current,win_check_outp)
            #print(lis)
            long = lis[0]
            short = lis[1]
            [next_val,date]=hc.pick_data()
            virtual_total = virtual_money(current,next_val)

            axis.append(i)
            if long == True:
                l_long = l_long + 1
            if short == True:
                l_short = l_short + 1
            if short == False and long == False:
                l_not = l_not + 1
            n=virtual_total
            #print(virtual_total)
            if (long==True):
                if(virtual_total >= 0) :
                    do = 0
                else:
                    do = do+1
            elif (short == True):
                if(virtual_total <= 0) :
                    do = 0
                else:
                    do = do + 1
            else:
                do=0
##            if(virtual_total > 0) :
##                do = do+1
##            else:
##                do = 0
    
print("total earnings = " + str(sum(day)))
print("total buys = " + str(l_long))
print("total sells = " + str(l_short))
print("total no trades = " + str(l_not))

ac = range(len(act_arr))
#pr = range(len(pred_arr))
plt.plot(ac, act_arr, 'r',label='actual value') 
plt.plot(ac, pred_arr, 'b',label='predicted label')
plt.legend()

#plt.plot(ac, last_arr, 'g')

#plt.show()



from sklearn.metrics import mean_squared_error
from math import sqrt

rms = sqrt(mean_squared_error(act_arr, pred_arr))

print("rmse : : " + str(rms))




    




    
        
    
