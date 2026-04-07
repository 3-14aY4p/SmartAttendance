from datetime import datetime
import pandas as pd
import numpy as np

from handlers import DBHandler as dh


def convert(time_text):
    # Functionality:
    # Converts a 24-hour time string into a Python time object.
    # OLD CODE KEPT FOR REFERENCE
    # format = '%I:%M%p'
    # time_str = datetime.strptime(time, "%H:%M").time()
    # return time_str

    return datetime.strptime(time_text, "%H:%M").time()