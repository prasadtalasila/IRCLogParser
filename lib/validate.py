def validate_RT_RL_CRT(in_data, ranges, fileName):
    """ 
        Validates the values of curve fit parameters

    Args:
        in_data(list): calculated values of curve fit parameters
        ranges(list of list):  expected values of curve fit parameters
        fileName(str): fileName

    Returns:
       null

    """
    for i in xrange(len(in_data)):
        if not ranges[i][0] <= in_data[i] <= ranges[i][1]:
            errorMessage (i, ranges[i], in_data[i], fileName)


def errorMessage(value_number, expected_range, actual_value, fileName):
    """ 
        Prints error messsage if value not as expected

    Args:
        value_number(int): index of the value in in_data which is not as expected
        expected_range(list): expected values of curve fit parameters
        actual_value(int):  calculated value of curve fit parameters
        fileName(str): fileName

    Returns:
       null

    """
    print "[Unexpected Value] of Arg", value_number, " @", fileName, "| EXPECTED_RANGE:", \
        expected_range, "| GOT:", actual_value