# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:15:25 2019

@author: irffy
"""

import pandas as pd
from fbprophet import Prophet
from datetime import datetime
from dateutil.relativedelta import relativedelta

df = pd.read_csv('C:/Users/irffy/OneDrive/Documents/Msc project files/MPS_LSOA_Level_Crime_Historic.csv') #obtain csv form lin in read me change file 
df['totals'] = df.iloc[:, 4:].sum(axis=0)
months = list(df.columns)[4:]
months.pop()
df2 = df.fillna(0)
monthlytotals = []

for i in months:
    monthlytotals.append(sum(list(df2[i])))
monthlytotals = [float(i) for i in monthlytotals]
months2 = [int(i) for i in months]
monthlies = dict(zip(months2, monthlytotals))

month = []
startDate = '2008-1-01'
endDate = '2019-1-01'

cur_date = start = datetime.strptime(startDate, '%Y-%m-%d').date()
end = datetime.strptime(endDate, '%Y-%m-%d').date()

while cur_date < end:
    print(cur_date)
    month.append(cur_date)
    cur_date += relativedelta(months=1) #generate list of months as datetime objects.
    
monthlydict = {'ds' : month,'y': monthlytotals}
monthlydf = pd.DataFrame(monthlydict)

timeseries = Prophet(seasonality_mode='multiplicative').fit(monthlydf) #generate time series object for monthly data 
future = timeseries.make_future_dataframe(periods=36, freq = 'M')#give monthly predictions for 36 months into the future
fcst = timeseries.predict(future)
fig2 = timeseries.plot(fcst)
fig = timeseries.plot_components(fcst)
