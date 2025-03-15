from google.protobuf.struct_pb2 import Struct, Value, ListValue

def dict_or_list_to_value(data):
    def _convert_value(v):
        if v is None:
            return Value(string_value="")
        if isinstance(v, dict):
            return Value(struct_value=dict_or_list_to_value(v))
        elif isinstance(v, list):
            list_value = ListValue()
            for item in v:
                item_value = _convert_value(item) 
                if item_value is not None:
                    list_value.values.append(item_value)
            return Value(list_value=list_value)
        elif isinstance(v, str):
            return Value(string_value=v)
        elif isinstance(v, bool):
            return Value(bool_value=v)
        elif isinstance(v, (int, float)):
            return Value(number_value=v)
        else:
            raise TypeError(f"Unsupported type: {type(v)}")

    if isinstance(data, dict): 
        struct = Struct()
        for k, v in data.items():
            struct.fields[k].CopyFrom(_convert_value(v))
        return struct
    elif isinstance(data, list): 
        list_value = ListValue()
        for item in data:
            item_value = _convert_value(item) 
            list_value.values.append(item_value)
        return list_value
    else:
        raise TypeError(f"Unsupported type at root level: {type(data)}")