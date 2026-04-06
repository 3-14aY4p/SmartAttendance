import datetime
import pandas as pd
import numpy as np

import DBHandler as dh



def convert(time):
    format = '%I:%M%p'
    time_str = datetime.strptime(time, "%H:%M").time()

    return time_str

