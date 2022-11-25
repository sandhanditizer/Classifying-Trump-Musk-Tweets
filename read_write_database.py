"""
Zachariah Kline
May 2, 2022
"""

import pickle

def write_database(database, filename):
    """
    Writes the calculated database to a binary file.\n
    File format: *.pkl.\n
    """
    pickle.dump(database, open(filename, 'wb'))
    
def read_database(filename):
    """
    Reads a binary file containing pickled database information.\n
    """
    return pickle.load(open(filename, 'rb'))