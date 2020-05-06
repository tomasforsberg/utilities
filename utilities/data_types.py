
def summarize_dtypes(df):
    dtypes_dict = {t.__str__(): [] for t in df.dtypes}
    for col, t in df.dtypes.items():
        dtypes_dict[t.__str__()].append(col)
    
    for t in dtypes_dict:
        print('|---------------------------------------')
        print('|', t, '\n|')
        for col in dtypes_dict[t]:
            print('|    ', col, ', sample: ', df[col].unique()[:3], '\n|')
