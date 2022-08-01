# encode: utf-8

import requests as req
from re import findall

# Jul 28, edu sites are in page range(1, 202)
# https://src.sjtu.edu.cn/rank/firm/0/?page=

baseUrl = 'https://src.sjtu.edu.cn/rank/firm/0/?page='

if __name__ == '__main__':
    for page in range(1, 202):
        print(page)
        url = baseUrl + str(page)
        res = req.get(url)
        schools = findall(r'href=\"/list/firm/[0-9]{4}\">([^"]+)</a>', res.text)
        school = ''
        for s in schools:
            school = school + s + '\n'
        with open('allSchoolName.txt', "a") as file:
            file.write(s)


