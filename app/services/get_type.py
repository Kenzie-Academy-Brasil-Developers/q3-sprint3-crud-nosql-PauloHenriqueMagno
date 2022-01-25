def get_type(value):
    value_type = str(type(value))[8:-2]

    if value_type == "str":
        value_type = "string"
    if value_type == "int":
        value_type = "integer"
    if value_type == "dict":
        value_type = "dictionary"
        
    return value_type