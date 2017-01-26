import plotly.plotly as py
import plotly.graph_objs as go
py.sign_in('rohangoel963', 'vh6le8no26')

def generate_group_bar_charts(y_values)
    trace1 = go.Bar(
        x=['#kubuntu-devel', '#ubuntu-devel','#kubuntu'],
        y=y_values[0],
        name='log(Number of Messages)'
    )
    trace2 = go.Bar(
        x=['#kubuntu-devel', '#ubuntu-devel','#kubuntu'],
        y=y_values[1],
        name='log(Number of Direct Messages)'
    )
    trace3 = go.Bar(
        x=['#kubuntu-devel', '#ubuntu-devel','#kubuntu'],
        y=y_values[2],
        name='log(Number of Users)'
    )

    data = [trace1, trace2, trace3]
    layout = go.Layout(
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    py.image.save_as(fig, "temp.png")

generate_group_bar_charts([
    [5.10114882,    5.0194652482, 4.9908093076],
    [4.5824497358,  4.7083614037,   4.3812775722],
    [2.6839471308,  3.0441476209,   3.6403820447]
])