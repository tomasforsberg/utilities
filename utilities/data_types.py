class dtype_summarizer:
    def __init__(self, df):
        self.d = {t.__str__(): {} for t in df.dtypes}
        for col, t in df.dtypes.items():
            self.d[t.__str__()][col] = df[col].unique()[:3]
        self.dtypes = list(self.d.keys())
        print('Available dtypes:', self.dtypes)
    
    def cols_of_type(self, t):
        return list(self.d[t].keys())
    
    def __str__(self):
        for t in self.d:
            print('|---------------------------------------')
            print('|', t, '\n|')
            for col in self.d[t]:
                print('|    ', col, ', sample: ', self.d[t][col], '\n|')
    
    def print_type(self, t):
        print('|---------------------------------------')
        print('|', t, '\n|')
        for col in self.d[t]:
            print('|    ', col, ', sample: ', self.d[t][col], '\n|')

