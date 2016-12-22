import plotly.plotly as py
import plotly.graph_objs as go
py.sign_in('rohangoel963', 'vh6le8no26')

trace1 = go.Bar(
    x=['#kubuntu-devel', '#ubuntu-devel','#kubuntu'],
    y=[5.10114882,	5.0194652482, 4.9908093076],
    name='log(Number of Messages)'
)
trace2 = go.Bar(
    x=['#kubuntu-devel', '#ubuntu-devel','#kubuntu'],
    y=[4.5824497358,	4.7083614037,	4.3812775722],
    name='log(Number of Direct Messages)'
)
trace3 = go.Bar(
    x=['#kubuntu-devel', '#ubuntu-devel','#kubuntu'],
    y=[2.6839471308,	3.0441476209,	3.6403820447],
    name='log(Number of Users)'
)

data = [trace1, trace2, trace3]
layout = go.Layout(
    barmode='group'
)

fig = go.Figure(data=data, layout=layout)
py.image.save_as(fig, "temp.png")


# NON LOGGED
# import plotly.plotly as py
# import plotly.graph_objs as go
# py.sign_in('rohangoel963', 'vh6le8no26')

# trace1 = go.Bar(
#     x=['#kubuntu-devel', '#ubuntu-devel','#kubuntu'],
#     y=[126226,  104584, 97906],
#     name='Number of Messages'
# )
# trace2 = go.Bar(
#     x=['#kubuntu-devel', '#ubuntu-devel','#kubuntu'],
#     y=[38234,   51093,  24059],
#     name='Number of Direct Messages'
# )
# trace3 = go.Bar(
#     x=['#kubuntu-devel', '#ubuntu-devel','#kubuntu'],
#     y=[483, 1107,   4369],
#     name='Number of Users'
# )

# data = [trace1, trace2, trace3]
# layout = go.Layout(
#     barmode='group'
# )

# fig = go.Figure(data=data, layout=layout)
# py.image.save_as(fig, "temp.png")