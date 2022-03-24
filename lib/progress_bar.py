def progress_bar(steps: int) -> str:
    """
    Function yields str progress bar: [ . . .    ] 50% completed
    param steps(int): amount of steps the progress bar has
    yields progressBar(str): current progress
    """
    str_lst = [' . . .'] * (steps + 3)
    str_lst[0] = '| '
    str_lst[-2] = ' |'
    index = 1
    for i in range(steps + 1):
        percent: str = str(round(100 * (index - 1) / steps))
        str_lst[-1] = f' {percent}% completed'

        yield "".join(str_lst)
        str_lst[index] = '###'
        index += 1
