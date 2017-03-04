import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error
import config
import util
import igraph
from random import randint
import math
import matplotlib.pyplot as plt
import os
import in_out.saver as saver
from numpy.random import normal
from scipy.optimize import curve_fit
from scipy import stats
import plotly.plotly as py
py.sign_in('rohangoel963', 'vh6le8no26')
import plotly.graph_objs as go

def generate_probability_distribution(data, initial_rows_filter):
    """ 
        Normalises y coordinates, dividing it by sum of all entries of y coordiantes

    Args:
        data(list of list): list of list representation csv data (with 2 coordinates)
        initial_rows_filter(int): analysis on first how many rows

    Returns:
        x-coordinate (list)
        freq (list) normalised-y-coordinates
    """
    topRows = [int(x[1]) for x in data[:initial_rows_filter]]
    total = sum(topRows)
    freq = [x/float(total) for x in topRows]
    
    return range(0, initial_rows_filter), freq


# FOR CL and RT anaylysis
def exponential_curve_fit_and_plot(data, initial_rows_filter, output_directory, output_file_name):
    """ 
        Fit to an expontial curve and draw the x-y data after filtering the intial initial_rows_filter rows

    Args:
        data(list of list): list of list representation csv data (with 2 coordinates)
        initial_rows_filter(int): analysis on first how many rows
        output_drectory(str): location to save graph
        output_file_name(str): name of the image file to be saved

    Returns:
        a (int) : curve fit variable for the equation a * np.exp(-b * x) + c
        b (int) : curve fit variable for the equation a * np.exp(-b * x) + c
        c (int) : curve fit variable for the equation a * np.exp(-b * x) + c
        mse (int) : Mean Squared error from the fit

    """

    x_pdf, y_pdf = generate_probability_distribution(data, initial_rows_filter)

    x = np.array(x_pdf)
    y = np.array(y_pdf)

    popt, pcov = curve_fit(util.exponential_curve_func, x, y)
    [a, b, c] = popt
    mse = mean_squared_error(util.exponential_curve_func(x, *popt), y)
    if config.DEBUGGER:
        print "CURVE FIT", output_file_name, "|", a, b, c, "MSE =", mse

    plt.figure()
    plt.plot(x, y, 'b-', label="Data")
    plt.plot(x, util.exponential_curve_func(x, *popt), 'r-', label="Fitted Curve")
    
    axes = plt.gca()
    axes.set_xlim([0, 20])
    axes.set_ylim([0, 1])
    plt.legend()
    # plt.show()
    plt.savefig(output_directory + "/" + output_file_name + ".png")
    plt.close()
    
    return [a, b, c, mse]


# Ignoring Initial Zeros in CRT
def exponential_curve_fit_and_plot_x_shifted(data, initial_rows_filter, output_directory, output_file_name):
    """ 
        Fit to an expontial curve and draw the x-y data after filtering the intial initial_rows_filter rows
        Also ignores the the input untill first non-zero y-coordinate and shifts the graph along
        y axes untill that first non-zero entry

    Args:
        data(list of list): list of list representation csv data (with 2 coordinates)
        initial_rows_filter(int): analysis on first how many rows
        output_drectory(str): location to save graph
        output_file_name(str): name of the image file to be saved

    Returns:
        a (int) : curve fit variable for the equation a * np.exp(-b * x) + c
        b (int) : curve fit variable for the equation a * np.exp(-b * x) + c
        c (int) : curve fit variable for the equation a * np.exp(-b * x) + c
        first_non_zero_index (int): amount by which the graph is shifted along y axis
        mse (int) : Mean Squared error from the fit

    """

    x_pdf, y_pdf = generate_probability_distribution(data, initial_rows_filter)

    first_non_zero_index = -1
    if filter(lambda x: x != 0, y_pdf):
        first_non_zero_index = y_pdf.index(filter(lambda x: x != 0, y_pdf)[0])

    x = np.array(x_pdf[0: initial_rows_filter - first_non_zero_index])
    y = np.array(y_pdf[first_non_zero_index:])

    popt, pcov = curve_fit(util.exponential_curve_func, x, y)
    [a, b, c] = popt
    mse = mean_squared_error(util.exponential_curve_func(x, *popt), y)
    if config.DEBUGGER:
        print "CURVE FIT", output_file_name, "|", a, b, c, "x-shift =", first_non_zero_index, "MSE =", mse
    
    plt.figure()
    plt.plot(x, y, 'b-', label="Data")
    plt.plot(x, util.exponential_curve_func(x, *popt), 'r-', label="Fitted Curve")
    
    axes = plt.gca()
    # axes.set_xlim([0 ,20])
    axes.set_ylim([0, 1])
    plt.xticks(range(0, 20, 5), xrange(first_non_zero_index, initial_rows_filter, 5), size='small')
    
    plt.legend()
    # plt.show()
    plt.savefig(output_directory + "/" + output_file_name + ".png")
    plt.close()

    return [a, b, c, mse, first_non_zero_index]


def plot_infomap_igraph(nx_graph, membership, output_directory, output_file_name, vertex_label_text=False, show_edges=True):
    """ 
    Plots  the informap community generated by igraph
    
    Args:
        nx_graph(object): networkx graph object
        membership(list): membership generated by infomap.community_infomap
        output_drectory(str): location to save graph
        output_file_name(str): name of the image file to be saved
        vertex_label_text(bool): toggle between lable text and index
        show_edges(bool): toggle to disable/enable edges during viz

    Returns:
        null
    """

    if membership is not None:
        graph_copy = nx_graph.copy()
        edges = []
        edges_colors = []
        for edge in nx_graph.es():
            if membership[edge.tuple[0]] != membership[edge.tuple[1]]:
                edges.append(edge)
                # edges_colors.append("#55555520")
                edges_colors.append("#00000000")
            else:
                edges_colors.append("#00000099")
        graph_copy.delete_edges(edges)
        layout = graph_copy.layout("kk")
        nx_graph.es["color"] = edges_colors
    else:
        layout = nx_graph.layout("kk")
        nx_graph.es["color"] = "gray"
    
    visual_style = {}
    visual_style["vertex_label_dist"] = 0
    visual_style["vertex_label_size"] = 18
    if show_edges:
        visual_style["edge_color"] = nx_graph.es["color"]
    else:
        visual_style["edge_color"] = "#00000000" 
    visual_style["vertex_size"] = 32
    visual_style["layout"] = layout
    visual_style["bbox"] = (1024, 768)
    visual_style["margin"] = 40
    visual_style["edge_label"] = nx_graph.es["weight"]
    visual_style["edge_width"] = igraph.rescale(nx_graph.es['weight'], out_range=(1, 10))
    
    for vertex in nx_graph.vs():
        if vertex_label_text:
            vertex["label"] = vertex["id"]
        else:
            vertex["label"] = vertex.index
        
    if membership is not None:
        colors = []
        for i in range(0, max(membership)+1):
            colors.append('%06X' % randint(0, 0xFFFFFF))
        for vertex in nx_graph.vs():
            vertex["vertex_shape"] = "circle"
            vertex["color"] = str('#') + colors[membership[vertex.index]]
            # coloring for channels vs users
            # vertex["vertex_shape"] = "square" if int(vertex["id"]) >= 1000000 else "circle"
            # vertex["color"] = "red" if int(vertex["id"]) >= 1000000 else "#00ff00"
        visual_style["vertex_color"] = nx_graph.vs["color"]
        visual_style["vertex_shape"] = nx_graph.vs["vertex_shape"]

    igraph.plot(nx_graph, (output_directory + "/" + output_file_name + ".png"), **visual_style)

    if config.DEBUGGER:
        print "INFOMAPS visualisation for", output_file_name, "completed"

def generate_log_plots (filter_val, plot_data, output_file_name, output_directory):
	"""
		Generate log plots for given time frame selecting first filter_val number ofan
		elements and plotting log of value on y axis.


	Args:
		filter_val (int): number of values to be used from data for plotting
		column_wise (list of list): data to be plotted
		output_drectory(str): location to save graph
		output_file_name(str): name of the image file to be saved

	Returns:
		null
	"""

	sum_each_row = []

	for row in plot_data[2:]: #ignore degree 0 and text, starting from degree 1
		sum_each_row.append(sum(row[1:]))

	# print sum_each_row
	x_axis_log = [math.log(i) for i in xrange(1, filter_val)]#ignore degree 0
	y_axis_log = [math.log(i) if i>0 else 0 for i in sum_each_row[1:filter_val] ]#ignore degree 01

	# get x and y vectors
	x = np.array(x_axis_log)
	y = np.array(y_axis_log)

	'''WAY TWO OF REGRESSION'''
	slope, intercept, r_value, p_value, std_err = stats.linregress(x_axis_log,y_axis_log)
	line = [slope*xi+intercept for xi in x_axis_log]

	print str(slope)+"\t"+str(intercept)+"\t"+str(r_value**2)+"\t"+str(mean_squared_error(y, line))

	if config.USE_PYPLOT:
		trace1 = go.Scatter(
		                  x=x,
		                  y=y,
		                  mode='lines',
		                  marker=go.Marker(color='rgb(255, 127, 14)'),
		                  name='Data'
		                  )

		trace2 = go.Scatter(
		                  x=x,
		                  y=line,
		                  mode='lines',
		                  marker=go.Marker(color='rgb(31, 119, 180)'),
		                  name='Fit'
		                  )

		layout = go.Layout(
		                title='DegreeNode',
		                # plot_bgcolor='rgb(229, 229, 229)',
		                  xaxis=go.XAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
		                  # yaxis=go.YAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)')
		                )

		data = [trace1, trace2]
		fig = go.Figure(data=data, layout=layout)

		py.image.save_as(fig, output_directory+"/"+output_file_name + ".png")

	else:
		#graph config
		axes = plt.gca()
		axes.set_xlim([0,3])
		axes.set_ylim([0,6])
		plt.xlabel("log(degree)")
		plt.ylabel("log(no_of_nodes)")

		# fit with np.polyfit
		m, b = np.polyfit(x, y, 1)

		plt.plot(x, y, '-')
		plt.plot(x, m*x + b, '-')
		plt.legend(['Data', 'Fit'], loc='upper right')
		plt.savefig(output_directory+"/" + output_file_name+".png")
		plt.close()
