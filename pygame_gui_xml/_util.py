_confirmation = ["true", "yes", "y", "enable", "enabled", "t"]
_rejection = ["false", "f", "no", "n", "disabled", "disable"]

def is_confirmation_string(strdata: str):
    return strdata in _confirmation

def is_rejection_string(strdata: str):
    return strdata in _rejection

def is_bool_string(strdata: str) -> bool:
    return is_confirmation_string(strdata.lower()) or is_rejection_string(strdata.lower())

def parse_bool_string(strdata: str) -> bool:
    if is_confirmation_string(strdata.lower()):
        return True
    elif is_rejection_string(strdata.lower()):
        return False
    raise ValueError(f' {strdata} determined to be neither a confirmation nor rejection string while parsing for boolean value ')

def is_num_str(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False

def is_int_str(string: str) -> bool:
    return is_num_str(string) and not "." in string

def is_float_str(string: str):
    return is_num_str(string) and "." in string