def validate_RT_RL(in_data, range_a, range_b, range_c, range_mse, fileName):
    a, b, c, mse = in_data

    if not range_a[0] <= a <= range_a[1]:
        print "[Unexpected Value] a      @", fileName, "| EXPECTED_RANGE:", range_a, "| GOT:", a

    if not range_b[0] <= b <= range_b[1]:
        print "[Unexpected Value] b      @", fileName, "| EXPECTED_RANGE:", range_b, "| GOT:", b

    if not range_c[0] <= c <= range_c[1]:
        print "[Unexpected Value] c      @", fileName, "| EXPECTED_RANGE:", range_c, "| GOT:", c

    if not range_mse[0] <= mse <= range_mse[1]:
        print "[Unexpected Value] mse    @", fileName, "| EXPECTED_RANGE:", range_mse, "| GOT:", mse


def validate_CRT(in_data, range_a, range_b, range_c, range_mse, expected_x_shift, fileName):
    a, b, c, mse, x_shift = in_data

    validate_RT_RL([a, b, c, mse], range_a, range_b, range_c, range_mse, fileName)

    if not expected_x_shift[0] <= x_shift <= expected_x_shift[1]:
        print "[Unexpected Value] x_shift @", fileName, "| EXPECTED_RANGE:", expected_x_shift, "| GOT:", x_shift