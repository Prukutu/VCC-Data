
import pandas as pd

def load_indicatorfile(datafile):
    """ Load the data from pre-processed NClimGrid files and
        process them.
    """

    df = pd.read_csv(datafile, parse_dates=['date'])

    newcols = {col: col[4:] for col in df.columns[1:]}
    df = df.rename(columns=newcols)
    df = df.dropna()
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')

    return df


def drop_spines(ax):
    
    # Move left and bottom spines outward by 10 points
    ax.spines.left.set_position(('outward', 10))
    ax.spines.bottom.set_position(('outward', 10))
    # Hide the right and top spines
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    
    return ax

def cdd(tavg, base=65):
    """ Compute annual cooling degree days"""

    df_cdd = tavg - base
    df_cdd[df_cdd < 0] = 0

    return df_cdd

def hdd(tavg, base=65):
    """ Compute annual cooling degree days"""
    df_hdd = base - tavg
    df_hdd[df_hdd < 0] = 0

    return df_hdd
