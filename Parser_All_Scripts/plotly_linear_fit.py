# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

import plotly.plotly as py
py.sign_in('rohangoel963', 'vh6le8no26')
import plotly.graph_objs as go

# Scientific libraries
from numpy import arange,array,ones
from scipy import stats
from sklearn.metrics import mean_squared_error


xi = [1,2,3,4,5,6]
# (Almost) linear sequence
y = [3,7,9,11,14,17]

# Generated linear fit
slope, intercept, r_value, p_value, std_err = stats.linregress(xi,y)
line = [slope*x+intercept for x in xi]

print str(slope)+"\t"+str(intercept)+"\t"+str(r_value)+"\t"+str(mean_squared_error(y, line))

# Creating the dataset, and generating the plot
trace1 = go.Scatter(
                  x=xi, 
                  y=y, 
                  mode='lines',
                  marker=go.Marker(color='rgb(255, 127, 14)'),
                  name='Data'
                  )

trace2 = go.Scatter(
                  x=xi, 
                  y=line, 
                  mode='lines',
                  marker=go.Marker(color='rgb(31, 119, 180)'),
                  name='Fit'
                  )

layout = go.Layout(
                title='Linear Fit in Python',
                # plot_bgcolor='rgb(0, 229, 229)',
                  # xaxis=go.XAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
                  # yaxis=go.YAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)')
                )

data = [trace1, trace2]
fig = go.Figure(data=data, layout=layout)

py.image.save_as(fig, "temp.png")