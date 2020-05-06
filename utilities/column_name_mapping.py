# To be used as result.format()
def fixed_width_formatter(fixed_width, padding='', alignment='left'):
    arrow = '<'
    if alignment == 'right':
        arrow = '>'
    elif alignment == 'center':
        arrow = '^'
    else:
        pass

    return '{:' + padding + arrow + str(fixed_width) + '}'

# Requires 1-to-1 maps
class TwoWayNameMapper:
    def __init__(self, name_dict=None):
        if name_dict is None:
            self.key_value_dict = {}
            self.value_key_dict = {}
        else:
            self.key_value_dict = name_dict
            self.value_key_dict = {}
            self.value_key_dict = {value: key for key, value in name_dict.items()}
        
        self.version = '1.0'
    
    def get_rename_dict(self):
        return self.key_value_dict
    
    def get_reverse_rename_dict(self):
        return self.value_key_dict
    
    def add(self, from_name, to_name):
        self.key_value_dict[from_name] = to_name
        self.value_key_dict[to_name] = from_name
    
    def add_dict(self, name_dict):
        for key, value in name_dict.items():
            self.key_value_dict[key] = value
            self.value_key_dict[value] = key
    
    def update(self, from_name, to_name):
        self.add(from_name, to_name)
    
    def update_dict(self, name_dict):
        self.add_dict(name_dict)
    
    def map(self, name):
        return self.key_value_dict.get(name, 'error: ' + name + ' not found')
    
    def reverse_map(self, name):
        return self.value_key_dict.get(name, 'error: ' + name + ' not found')
    
    def print(self):
        keys = self.key_value_dict.keys()
        max_key_len = max([len(x) for x in keys])
        for key in keys:
            print(fixed_width_formatter(max_key_len, padding='_').format(key), '<->', self.key_value_dict.get(key, 'error: ' + key + ' not found'))
    
    def print_modified(self):
        modified_keys =  [x for x, y in self.key_value_dict.items() if x != y]
        if len(modified_keys) == 0:
            print('No name mappings have been modified')
            return
        
        max_key_len = max([len(x) for x in modified_keys])
        for key in modified_keys:
            print(fixed_width_formatter(max_key_len, padding='_').format(key), '<->', self.key_value_dict.get(key, 'error: ' + key + ' not found'))
    
    def map_column_names(self, df):
        return df.columns.map(self.key_value_dict)
    
    def reverse_map_column_names(self, df):
        return df.columns.map(self.value_key_dict)

def default_name_mapper(df):
    return TwoWayNameMapper({col: col for col in df.columns})


