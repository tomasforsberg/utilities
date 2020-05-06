import numpy as np
import pandas as pd

# Adds normally distributed noise to value or array
def jitter(x, std=0.01):
    if isinstance(x, str) or isinstance(x, dict):
        print('Unsupported type in jitter function (str or dict)')
        return x
    if hasattr(x, '__len__'):
        return x + np.random.normal(0, std, len(x))
    else:
        return x + np.random.normal(0, std)

# Applies np.log while avoiding negative values by capping at some value close to zero
def cap_and_log(x, cap=0.01):
    if hasattr(x, 'shape'):
        return np.log(np.maximum(0.01 * np.ones(x.shape), x))
    else:
        return np.log(np.maximum(0.01, x))

def days_between_dates(d, rel_d):
    if isinstance(d, str):
        return (pd.to_datetime(d) - pd.to_datetime(rel_d)).days
    elif hasattr(d, 'apply'):
        return (pd.to_datetime(d) - 
                pd.to_datetime(rel_d)).apply(lambda x: x.days)
    elif hasattr(d, '__len__'):
        return [(pd.to_datetime(x) - pd.to_datetime(rel_d)).days for x in d]
    else:
        print('Unsupported type in days_between_dates')
        return d
        
