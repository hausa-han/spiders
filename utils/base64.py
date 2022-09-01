import base64 as b64


def encode(s, charset='utf-8'):
    s = str.lower(s)
    return b64.b64encode(s.encode(charset)).decode(charset)


def decode(s, charset='utf-8'):
    s = str.lower(s)
    return b64.b64decode(s.encode(charset)).decode(charset)


if __name__ == '__main__':
    print(decode('PGh0bWw+DQo8dGl0bGU+SGVyZSdzIGEgc2VjcmV0LiBDYW4geW91IGZpbmQgaXQ/PC90aXRsZT4NCjw/cGhwDQoNCmlmKGlzc2V0KCRfR0VUWydmaWxlJ10pKXsNCiAgICAkZmlsZSA9ICRfR0VUWydmaWxlJ107DQogICAgaW5jbHVkZSgkZmlsZSk7DQp9ZWxzZXsNCiAgICBoaWdobGlnaHRfZmlsZShfX0ZJTEVfXyk7DQp9DQo/Pg0KPC9odG1sPg0K'))