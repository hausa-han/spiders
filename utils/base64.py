import base64 as b64


def encode(s, charset='utf-8'):
    s = str.lower(s)
    return b64.b64encode(s.encode(charset)).decode(charset)


def decode(s, charset='utf-8'):
    s = str.lower(s)
    return b64.b64decode(s.encode(charset)).decode(charset)


if __name__ == '__main__':
    print(decode('CMsBEJZOGAAiAk9LKAEyJ9oMJBiUgKTK0tf5AiAuKAAwAzj2bkCUgKTK0tf5AkjQu4LDltn5AjoiMjAyMjA4MjgwMDAyNDAwMTAyMTEyMTkwMTQwMzg0NTAzMVDY/KmArjBYzf6pgK4waMTW5tHcAg=='))