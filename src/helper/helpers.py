import copy

def setDefaultValue(field, data, default):
    return data[field] if field in data and data[field] != None else default