import requests
import hashlib
import re
import os

cookie = ''

url = {
    'loginurl': 'http://jxglxt2.haust.edu.cn/_data/index_LOGIN.aspx',
    'before_getscore_url': 'http://jxglxt2.haust.edu.cn/xscj/Stu_MyScore.aspx',
    'scoretexturl': 'http://jxglxt2.haust.edu.cn//xscj/Stu_MyScore_rpt.aspx',
    'scorepicurl': 'http://jxglxt2.haust.edu.cn/xscj/Stu_MyScore_Drawimg.aspx?x=1&h=2&w=726&xnxq=20191&xn=2019&xq=1&rpt=1&rad=2&zfx=0&xh='
}

login_header = {
    'Host': 'jxglxt2.haust.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://jxglxt2.haust.edu.cn',
    'Connection': 'keep-alive',
    'Referer': 'http://jxglxt2.haust.edu.cn/_data/index_LOGIN.aspx',
    'Cookie': '',
    'Upgrade-Insecure-Requests': '1'
}

score_header = {
    'Host': 'jxglxt2.haust.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'image/webp,*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Referer': 'http://jxglxt2.haust.edu.cn/xscj/Stu_MyScore_rpt.aspx',
    'Cookie': ''
}

before_getscore_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': '',
    'Host': 'jxglxt1.haust.edu.cn',
    'Referer': 'http://jxglxt1.haust.edu.cn/frame/menu.aspx',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

scoretext_header = {
    'Host': 'jxglxt1.haust.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '96',
    'Origin': 'http://jxglxt1.haust.edu.cn',
    'Connection': 'keep-alive',
    'Referer': 'http://jxglxt1.haust.edu.cn/xscj/Stu_MyScore.aspx',
    'Cookie': '',
    'Upgrade-Insecure-Requests': '1',
    'X-Forwarded-For': '127.0.0.1'
}

scoredata = {
    'sel_xn': '',
    'sel_xq': '',
    'SJ': '1',
    'btn_search': '%BC%EC%CB%F7',
    'SelXNXQ': '2',
    'txt_xm': '201900002719',
    'zfx_flag': '0',
    'zxf': '0'
}


def setcookie(cookie):
    login_header['Cookie'] = 'name=value;name=value;ASP.NET_SessionId=' + cookie
    score_header['Cookie'] = 'name=value;name=value;ASP.NET_SessionId=' + cookie
    scoretext_header['Cookie'] = 'name=value;name=value;ASP.NET_SessionId=' + cookie
    before_getscore_header['Cookie'] = 'name=value;name=value;ASP.NET_SessionId=' + cookie


def encodedpasswd(stuID, passwd):
    print("正在加密密码")
    a = hashlib.md5()
    a.update(passwd.encode(encoding='utf-8'))
    str = a.hexdigest()
    str = stuID + str[:-2] + '10464'
    b = hashlib.md5()
    str = str.upper()
    b.update(str.encode(encoding='utf-8'))
    str = b.hexdigest()
    str = str.upper()
    print("加密完成：" + str[:-2] + '\n')
    return str[:-2]


def getcookie():
    print('正在进行第一次请求，以获取Cookies')
    url = 'http://jxglxt2.haust.edu.cn/'
    cookies = requests.get(url).cookies
    # 由于这时的Cookies是RequestsCookieJar类型，所以要进行转换：
    cookies = requests.utils.dict_from_cookiejar(cookies)
    print('Cookies获取成功：' + cookies['ASP.NET_SessionId'] + '\n')
    return cookies['ASP.NET_SessionId']


def sorry():
    print('请将此错误向作者反馈，或在GitHub/Gitee上提出问题')
    print('作者邮箱：572157852@qq.com')
    print('\n感谢您的使用~~~~\n')
    exit()


def setscoredata():
    r = requests.get(url['before_getscore_url'], headers=before_getscore_header).text
    # print(r)
    sel_xn = re.findall(r'value=\'([^"]+)\'', r)
    scoredata['sel_xn'] = sel_xn[0][0:4]
    sel_xq = re.findall(r'Col2\[0\]=\'([^"]+)\'', r)
    scoredata['sel_xq'] = sel_xq[0][0:1]
    txt_xm = re.findall(r'name=\"txt_xm\"([^"]+)', r)
    txt_xm = txt_xm[0][7:19]
    scoredata['txt_xm'] = txt_xm
    url['scorepicurl'] += txt_xm


def getscore():
    setscoredata()
    rscoretext = requests.post(url['scoretexturl'], headers=scoretext_header, data=scoredata)
    rscore = requests.get(url['scorepicurl'], headers=score_header)
    if rscore.text.find('JFIF') != -1:
        print('成绩获取成功，正在保存成绩图片......')
        f = open('score.jfif', 'wb')
        f.write(rscore.content)
        f.close()
        print('图片保存成功！\n请打开score.jfif查看成绩')
        print('感谢您使用此脚本\n祝您生活愉快~~\n')
        exit()
    else:
        print('图片获取失败！')
        sorry()


def login(stuID, passwd):
    print('正在进行登录操作')
    logindata = {
        '__VIEWSTATE': 'dDwxNDQzMTI4MDI2O3Q8O2w8aTwwPjtpPDE+O2k8Mj47aTwzPjs+O2w8dDxwPGw8VGV4dDs+O2w85rKz5Y2X56eR5oqA5aSn5a2mOz4+Ozs+O3Q8cDxsPFRleHQ7PjtsPFxlOz4+Ozs+O3Q8O2w8aTwxPjs+O2w8dDw7bDxpPDA+Oz47bDx0PHA8bDxUZXh0Oz47bDxcPG9wdGlvbiB2YWx1ZT0nU1RVJyB1c3JJRD0n5a2m44CA5Y+3J1w+5a2m55SfXDwvb3B0aW9uXD4KXDxvcHRpb24gdmFsdWU9J1RFQScgdXNySUQ9J+W3peOAgOWPtydcPuaVmeW4iOaVmei+heS6uuWRmFw8L29wdGlvblw+Clw8b3B0aW9uIHZhbHVlPSdTWVMnIHVzcklEPSfluJDjgIDlj7cnXD7nrqHnkIbkurrlkZhcPC9vcHRpb25cPgpcPG9wdGlvbiB2YWx1ZT0nQURNJyB1c3JJRD0n5biQ44CA5Y+3J1w+6Zeo5oi357u05oqk5ZGYXDwvb3B0aW9uXD4KOz4+Ozs+Oz4+Oz4+O3Q8cDxwPGw8VGV4dDs+O2w85Y+R55Sf5pyq55+l6ZSZ6K+v77yBXDxiclw+55m75b2V5aSx6LSl77yBOz4+Oz47Oz47Pj47PqJLbwpNx1b436KMIO//FKm/wdri',
        '__VIEWSTATEGENERATOR': 'CAA0A5A7',
        'Sel_Type': 'STU',
        'txt_sdsdfdsfryuiighgdf': stuID,
        'txt_dsfdgtjhjuixssdsdf': '',
        'txt_sftfgtrefjdndcfgerg': '',
        'typeName': '%D1%A7%C9%FA',
        'sdfdfdhgwerewt': passwd,
        'cxfdsfdshjhjlk': ''
    }
    rlogin = requests.post(url['loginurl'], headers=login_header, data=logindata)
    if rlogin.text.find('正在加载权限数据') != -1:
        print('登陆成功！正在获取成绩\n')
        getscore()
    else:
        print('登录失败！请检查输入的账号密码是否正确......\n若输入无误\n')
        sorry()


if __name__ == '__main__':
    stuID = ''
    passwd = ''
    os.system('color a')
    try:
        f = open('logindata.txt', 'r')
        stuID = f.readline()
        passwd = f.readline()
    except FileNotFoundError:
        os.system('echo >> logindata.txt')
    if stuID == '':
        stuID = input("请输入您的学号：")
        passwd = input("请输入密码：")
        passwd = encodedpasswd(stuID, passwd)
        print('将自动存储加密后的账号密码')
        f = open('logindata.txt', 'w')
        f.write(stuID + '\n')
        f.write(passwd)
    setcookie(getcookie())
    login(stuID, passwd)
