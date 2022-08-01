import requests as req
from re import findall
from time import sleep

baseUrl = 'https://src.sjtu.edu.cn/rank/firm/0/?page='

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'
}

if __name__ == '__main__':
    with open('allSchoolName.txt', 'r') as file:
        school = file.readline()
        school = school[:-1]
        i = 1
        while school != '':
            print(str(i) + '/3007: ' + school, end=': ')
            try:
                res = req.get('https://cn.bing.com/search?q=' + school + '+官网', headers=header)
            except:
                print('Error, retry:')
                sleep(20)
                continue
            href = findall(r'class="sh_favicon" href="([^"]+)" h', res.text)
            while href[0][-1] != '/':
                href[0] = href[0][:-1]
            print(href[0])
            with open('allSchoolSiteRoot.txt', "a") as f:
                f.write(href[0] + '\n')
            school = file.readline()
            school = school[:-1]
            i = i + 1
