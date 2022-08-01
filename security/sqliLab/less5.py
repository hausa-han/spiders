import requests as req


def checkRes(s):
    if 'You are in' in s:
        return True
    else:
        return False


baseurl = 'http://a686e576-f16c-4c1a-9dcc-36b29632ddae.node4.buuoj.cn/Less-5/?id=1'

res = req.get(baseurl + '\'')
print(checkRes(res.text))

