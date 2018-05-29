import matplotlib as mpl
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
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
import lib.in_out.saver as saver
from numpy.random import normal
from scipy.optimize import curve_fit
from scipy import stats
from numpy import genfromtxt
import glob

def plot_data (data, output_directory, output_file_name):
    x_data, y_data = (d for d in data)

    x = np.array(x_data)
    y = np.array(y_data)

    plt.figure()
    plt.plot(x, y, 'b-', label="Data")
    
    plt.legend()
    # plt.show()
    saver.check_if_dir_exists(output_directory)
    plt.savefig(output_directory + "/" + output_file_name + ".png")
    plt.close()


def generate_probability_distribution(data):
    """ 
        Normalises y coordinates, dividing it by sum of all entries of y coordiantes

    Args:
        data(list of list): list of list representation csv data (with 2 coordinates)

    Returns:
        x-coordinate (list)
        freq (list) normalised-y-coordinates
    """
    if data:
        topRows = [int(x[1]) for x in data]
        total = sum(topRows)
        freq = [x/float(total) for x in topRows]
    
        return range(0, len(data)), freq
    else:
        print "ERROR generate_probability_distribution"
        return -1, -1


# FOR CL and RT anaylysis
def exponential_curve_fit_and_plot(data, output_directory, output_file_name):
    """ 
        Fit to an expontial curve and draw the x-y data

    Args:
        data(list of list): list of list representation csv data (with 2 coordinates)
        output_drectory(str): location to save graph
        output_file_name(str): name of the image file to be saved

    Returns:
        a (int) : curve fit variable for the equation a * np.exp(-b * x) + c
        b (int) : curve fit variable for the equation a * np.exp(-b * x) + c
        c (int) : curve fit variable for the equation a * np.exp(-b * x) + c
        mse (int) : Mean Squared error from the fit

    """

    x_pdf, y_pdf = generate_probability_distribution(data)

    if y_pdf != -1:
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
        saver.check_if_dir_exists(output_directory)
        plt.savefig(output_directory + "/" + output_file_name + ".png")
        plt.close()
        
        return [a, b, c, mse]


# Ignoring Initial Zeros in CRT
def exponential_curve_fit_and_plot_x_shifted(data, output_directory, output_file_name):
    """ 
        Fit to an expontial curve and draw the x-y data
        Also ignores the the input untill first non-zero y-coordinate and shifts the graph along
        y axes untill that first non-zero entry

    Args:
        data(list of list): list of list representation csv data (with 2 coordinates)
        output_drectory(str): location to save graph
        output_file_name(str): name of the image file to be saved

    Returns:
        a (int) : curve fit variable for the equation a * np.exp(-b * x) + c
        b (int) : curve fit variable for the equation a * np.exp(-b * x) + c
        c (int) : curve fit variable for the equation a * np.exp(-b * x) + c
        first_non_zero_index (int): amount by which the graph is shifted along y axis
        mse (int) : Mean Squared error from the fit

    """

    x_pdf, y_pdf = generate_probability_distribution(data)

    if y_pdf != -1:
        first_non_zero_index = -1
        if filter(lambda x: x != 0, y_pdf):
            first_non_zero_index = y_pdf.index(filter(lambda x: x != 0, y_pdf)[0])

        x = np.array(x_pdf[0: -1*first_non_zero_index])
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
        plt.xticks(range(0, 20, 5), xrange(first_non_zero_index, len(x), 5), size='small')
        
        plt.legend()
        # plt.show()
        saver.check_if_dir_exists(output_directory)
        plt.savefig(output_directory + "/" + output_file_name + ".png")
        plt.close()

        return [a, b, c, mse, first_non_zero_index]


def plot_infomap_igraph(i_graph, membership, output_directory, output_file_name, show_edges=True, aux_data=None):
    """ 
    Plots  the informap community generated by igraph
    
    Args:
        i_graph(object): igraph graph object
        membership(list): membership generated by infomap.community_infomap
        output_drectory(str): location to save graph
        output_file_name(str): name of the image file to be saved
        show_edges(bool): toggle to disable/enable edges during viz

    Returns:
        null
    """

    if membership is not None:
        graph_copy = i_graph.copy()
        edges = []
        edges_colors = []
        for edge in i_graph.es():
            if membership[edge.tuple[0]] != membership[edge.tuple[1]]:
                edges.append(edge)
                edges_colors.append("#55555520")
                # edges_colors.append("#00000000")
            else:
                edges_colors.append("#00000099")
        graph_copy.delete_edges(edges)
        layout = graph_copy.layout("kk")
        i_graph.es["color"] = edges_colors
    else:
        layout = i_graph.layout("kk")
        i_graph.es["color"] = "gray"
    
    visual_style = {}
    visual_style["vertex_label_dist"] = 0
    visual_style["vertex_label_size"] = 18
    if show_edges:
        visual_style["edge_color"] = i_graph.es["color"]
    else:
        visual_style["edge_color"] = "#00000000" 
    visual_style["vertex_size"] = 32
    visual_style["layout"] = layout
    visual_style["bbox"] = (1024, 768)
    visual_style["margin"] = 40
    #visual_style["edge_label"] = i_graph.es["weight"]
    if i_graph.es:
        visual_style["edge_width"] = igraph.rescale(i_graph.es['weight'], out_range=(1, 10))
    
    for vertex in i_graph.vs():
        vertex["label"] = vertex.index
        
    if membership is not None:
        colors = []
        for i in range(0, max(membership)+1):
            colors.append('%06X' % randint(0, 0xFFFFFF))
        for vertex in i_graph.vs():
            vertex["vertex_shape"] = "circle"
            vertex["color"] = str('#') + colors[membership[vertex.index]]
            # coloring for channels vs users
            vertex["vertex_shape"] = "square" if (vertex["id"].isdigit() and int(vertex["id"]) >= 1000000) else "circle"
            # vertex["color"] = "red" if (vertex["id"].isdigit() and int(vertex["id"]) >= 1000000) else "#00ff00"
            
            if aux_data:
                if aux_data["type"] == "MULTI_CH":
                    # ['#kubuntu-devel', '#kubuntu', '#ubuntu-devel']
                    color_nodes = ["#ff0000", "#00ff00", "#0000ff"]
                    vertex["color"] = color_nodes[np.argmax(aux_data["uc_adj"][aux_data["user_hash"].index(vertex["id"])])]
        if not aux_data:
            visual_style["vertex_color"] = i_graph.vs["color"]
        visual_style["vertex_shape"] = i_graph.vs["vertex_shape"]
        
    saver.check_if_dir_exists(output_directory)
    igraph.plot(i_graph, (output_directory + "/" + output_file_name + ".png"), **visual_style)

    if config.DEBUGGER:
        print "INFOMAPS visualisation for", output_file_name, "completed"


def generate_log_plots(plot_data, output_directory, output_file_name):
    """
        Generate log plots for given time frame


    Args:
        plot_data (list of list): data to be plotted
        output_drectory(str): location to save graph
        output_file_name(str): name of the image file to be saved

    Returns:
        slope : The slope of linear fit for the log plot.
        r_square :
        mean_sqaure_error : Mean sqaure error for best fit.
    """

    sum_each_row = []

    for row in plot_data[2:]:   #ignore degree 0 and text, starting from degree 1
        sum_each_row.append(row)

    x_axis_log = [math.log(i) for i in xrange(1, len(sum_each_row) + 1)]
    y_axis_log = [math.log(i) if i>0 else 0 for i in sum_each_row[0:] ] 

    slope,intercept,r_square,mean_squared_error = calc_plot_linear_fit(x_axis_log, y_axis_log, output_directory, output_file_name)
    
    return slope,intercept,r_square,mean_squared_error

def calc_plot_linear_fit(x_in, y_in, output_directory, output_file_name):
    """
        Calculate and plot linar fit for data


    Args:
        x_in (list of int): x_axis data
        y_in (list of int): y_axis data
        output_drectory(str): location to save graph
        output_file_name(str): name of the image file to be saved

    Returns:
        null
    """
    # get x and y vectors
    if x_in and y_in: 
        x = np.array(x_in)
        y = np.array(y_in)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_in, y_in)
        line = [slope*xi+intercept for xi in x_in]

        print str(slope)+"\t"+str(intercept)+"\t"+str(r_value**2)+"\t"+str(mean_squared_error(y, line))
        saver.check_if_dir_exists(output_directory)

        axes = plt.gca()
        axes.set_xlim([0, 3])
        axes.set_ylim([0, 6])
        plt.xlabel("log(degree)")
        plt.ylabel("log(no_of_nodes)")

        # fit with np.polyfit
        m, b = np.polyfit(x, y, 1)

        plt.plot(x, y, '-')
        plt.plot(x, m*x + b, '-')
        plt.legend(['Data', 'Fit'], loc='upper right')
        plt.savefig(output_directory+"/" + output_file_name+".png")
        plt.close()
            
        return slope,intercept,r_value**2,mean_squared_error(y, line)
    else:
        print "ERROR calc_plot_linear_fit"
        return -1, -1, -1, -1


def matplotlob_csv_heatmap_generator(csv_file, output_directory, output_file_name):
    """
        Plots heatmaps for all the csv files in the given directory
        Can be used as a script for generating heatmaps, faster alternative to plotly

    Args:
        in_directory (str):  location of input csv files
        output_drectory(str): location to save graph
        output_file_name(str): name of the image file to be saved

    Returns:
        null
    """
    
    column_labels = map(str, range(1, 32))
    row_labels = map(str, range(1, 49))
    
    data = genfromtxt(csv_file, delimiter=',')
    print(data)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    heatmap = ax.pcolor(data, cmap=plt.cm.Reds)

    cbar = plt.colorbar(heatmap)

    def np_arrange_helper(data, disp):
        return np.arange(data) + disp

    # put the major ticks at the middle of each cell
    ax.set_xticks(np_arrange_helper(data.shape[0], 0.5), minor=False)
    ax.set_yticks(np_arrange_helper(data.shape[1], 0.5), minor=False)

    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    ax.set_xticklabels(row_labels, minor=False)
    ax.set_yticklabels(column_labels, minor=False)
    
    plt.savefig(output_directory+"/" + output_file_name+".png")
    plt.close()


def box_plot(data, output_directory, output_file_name):
    """
        Plots Box Plots

    Args:
        data (list):  data
        output_drectory(str): location to save graph
        output_file_name(str): name of the image file to be saved

    Returns:
        null
    """
    plt.figure()
    plt.boxplot(data)
    
    plt.legend()
    saver.check_if_dir_exists(output_directory)
    plt.savefig(output_directory + "/" + output_file_name + ".png")
    plt.close()
