import pandas as pd

# Sanity check before merging
def pre_merge_report(df1, df2, how, key, key_2=None):
    if key_2 is None:
        key_2 = key
    df1_unique_keys = df1[key].unique()
    df2_unique_keys = df2[key_2].unique()
    return pd.DataFrame(
        data={
            'shape': [df1.shape, df2.shape, df1.merge(df2, how=how, left_on=key, right_on=key_2).shape], 
            'unique keys': [len(df1_unique_keys), len(df2_unique_keys), ''], 
            'keys not in other': [
                len([x for x in df1_unique_keys if x not in df2_unique_keys]), 
                len([x for x in df1_unique_keys if x not in df2_unique_keys]), 
                ''
            ]},
        index=['DF 1', 'DF 2', 'Merged'])

