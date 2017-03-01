

def cookies_to_dict(str_cookies):
    assert isinstance(str_cookies, str), 'Cookies should be a str'
    dict_cookies = {}
    for kv in str_cookies.split(';'):
        k, v = kv.strip().split('=', 1)
        dict_cookies[k] = v
    return dict_cookies
