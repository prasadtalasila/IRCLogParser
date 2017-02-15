import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error
import config
import util

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
