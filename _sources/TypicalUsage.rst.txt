Typical Usage Of IRCLogParser
*****************************

IRCLogParser currently uses a config.py file to configure and tweak the behaviour of functions. The settings in config.py can be found here_ which can be changed as per requirements.

.. _here: https://github.com/prasadtalasila/IRCLogParser/blob/v1.0.0/lib/config.py


Below we show how one can use functions of IRCLogParser to analyse their logs. The analysis and the code is completely modularised and hence is presented in a modular structure :


Input
=====

Reading the logs is typically the first step to analysis logs assuming that the logs aren't already stored in a data-structure.

.. code-block:: python
    
    from irclogparser.in_out import reader
    import irclogparser.nickTracker as nickTracker

    # reads the log files from the disk
    log_data = reader.linux_input(log_directory, channel_name, starting_date, ending_date)
    
    # identify the all the nicks (nicks), and the nicks which refer to the same user (nick_same_list)
    nicks, nick_same_list = nickTracker.nick_tracker(log_data) 


Analysis & Output
=================

IRCLogParser gives various functions for analysis your logs. A few of which are demonstrated below:

.. code-block:: python

    from irclogparser.analysis import network
    from irclogparser.in_out import saver

    # analyse logs to generate message_number_graph in which is a network graph object
    message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)

    # use saver module to save (draw) the networkx graph returned above at the specified location
    saver.draw_nx_graph(message_number_graph, "/home/rohan/Desktop", "file_name_message_number_graph")


The above code snippet is for bulk analysis. If someone wants to plot the graph on a day by day basis, one could just enable the boolen.

.. code-block:: python
    
    # make the boolean to be True for a day by day analysis, the returned object is now a list of graphs (one for each day)
    message_number_graph_day_list = network.message_number_graph(log_data, nicks, nick_same_list, True)

    # use saver module to save (draw) the networkx graph returned above at the specified location for every graph in the list
    for i in range(len(message_number_graph_day_list)):
        saver.draw_nx_graph(message_number_graph_day_list[i][0], "/home/rohan/Desktop", "message_number_" + str(i+1))

Another example could be analysis of response time:

.. code-block:: python
    
    from irclogparser.analysis import channel
    
    # analyse the logs for response time this time
    resp_time = channel.response_time(log_data, nicks, nick_same_list)

    # save the generated list of lists as csv for later reference
    saver.save_csv(resp_time, "/home/rohan/Desktop", "csv_file_name_resp_time")


Visualisation
=============

It is also possible for a researcher to visualise his analysis by using the vis module provided by IRCLogParser. The same module also takes care for fitting the curves during the visualisation process.

.. code-block:: python
    
    import irclogparser.vis as vis
    
    # let's curve fit and visualise the analysis for response time generated in the snippet above
    # this generates and saves the png for the graph generated after fitting at specified location
    # the function returns the fit parameters generated after fitting the graph to the equation specified # the fit parameters are stored in the variable resp_time_curve_fit_parameters here 
    # which can be used to ascertain the quality of plot (and analysis)
    resp_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot(resp_time, 20, "/home/rohan/Desktop", "png_name_resp_time")

    #obviously one can just plot the graph along with the fit without caring about the parameters
    vis.exponential_curve_fit_and_plot(resp_time, 20, "/home/rohan/Desktop", "png_name_resp_time")

Note: Since all the modules of IRCLogParser are independant of each other, one could use any module without relying on the analysis from some other module. For example, a user can use the vis module to visualise something which has nothing to do with logs ans parsing:

 .. code-block:: python
    
    import irclogparser.vis as vis
    
    custom_list = [[1, 2],[2, 4],[3, 6],[4, 10],[5, 12],[6, 14]]
    vis.exponential_curve_fit_and_plot(, 2, "/home/rohan/Desktop", "png_name_custom")


Validation
==========

One can also validate results: ensure that the curve fits are in expected range. Here is an example:

 .. code-block:: python
    
    import irclogparser.validate as validate
    
    # ensures that the curve fit parameters (here : a, b, c, mse) are in the specified range
    # throws an error (and logs) otherwise
    validate.validate_RT_RL_CRT(resp_time_curve_fit_parameters, 
        [[0.3, 10.4], [10.3, 30.4], [-0.002, 0.002], [0, 0.002]], "resp_time")

Miscellaneous
=============
An example of community analysis from scratch:

.. code-block:: python
    
    from irclogparser.in_out import reader, saver
    import irclogparser.nickTracker as nickTracker
    from irclogparser.analysis import community, network
    import irclogparser.vis as vis
    
    # firstly change analysis to all channels in config

    # 1. Input and build nicks and nick_same_list
    log_data = reader.linux_input(log_directory, channel_name, starting_date, ending_date)
    nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(log_data, True)
    
    # 2. Analysis
    dict_out, graph = network.channel_user_presence_graph_and_csv(nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash)

    # 3. Output
    saver.save_net_nx_graph(dict_out["UU"]["reducedMatrix"],"/home/rohan/Desktop", "adjCC")

    # 3.1 generate the community graph (igraph) and the membership info by using the .net file
    adjCC_graph, adjCC_membership = community.infomap_igraph(ig_graph=None, net_file_location="/home/rohan/Desktop/adjCC.net")

    # 4. Visualisation
    vis.plot_infomap_igraph(adjCC_graph, adjCC_membership, output_directory, "adjCC_infomaps")


One could also see sample.py_ which comes along with library for more examples.

.. _sample.py: https://github.com/prasadtalasila/IRCLogParser/blob/v1.0.0/sample.py