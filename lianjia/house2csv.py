# -*- coding: utf-8 -*-

'''
导入各种包，其中：
re.findall用来进行正则匹配
csv用来写csv文件
asyncio和aiohttp用来配合进行异步协程爬虫开发
time用来记录运行时间
logging用来显示错误日志
'''
from re import findall
import csv
import asyncio
import aiohttp
import time
import logging
import operator

# 定义基本url和行政区域列表
baseurl = "https://cd.lianjia.com/zufang"
block_list = ["锦江", "青羊", "武侯", "高新", "成华", "金牛", "天府新区", "高新西"]
# 定义session和最大允许开启的协程数量，这个数越大，爬的越快
session = None
semaphore = asyncio.Semaphore(8)

'''
这个函数定义了一个基本的用来实现一个使用get方法获取目标网页html文本的接口，相当于requests.get
input: A URL
output: This URL's HTML
'''


async def get(url):
    async with semaphore:
        try:
            logging.info('Getting %s', url)
            async with session.get(url) as response:
                return await response.text()
        except aiohttp.ClientError:
            logging.error('Error occurred while getting %s', url, exc_info=True)


# 这个函数用来获取每个行政分区对应的URL
def get_blockurls(html):
    result = []
    for block in block_list:
        block_url = findall(r'href="/zufang(.*?)"  >' + block, html)[0]
        result.append(block_url)
    return result


# 这个函数用来获取子区域的区域名
def get_subblock(html):
    result = []
    html = html.replace("\n", "").replace("\r", "").replace("\t", "").replace(" ", "")
    temp = findall(r'--level3"><ahref="/zufang(.*?)</a>', html)
    for t in temp:
        result.append(t.split('">')[1])
    return result


# 这个函数用来获取每个区域的房间数量
def get_roomnum(html):
    result = 0
    result = findall(r'content__title--hl">(.*?)</span>', html)[0]
    return result


# 这个函数获得各个房间的URL
async def get_roomurls(html, num):
    result = []
    pagenum = int((num - (num % 30)) / 30) + 1
    html = html.replace("\n", "").replace("\r", "").replace("\t", "").replace(" ", "")
    urls = findall(r'class="content__list--item--aside"target="_blank"href="/zufang(.*?)"title="', html)
    for u in urls:
        result.append(baseurl + u)
    for p in range(2, pagenum + 1):
        html = await get(baseurl + "/pg" + str(p) + "/#contentList")
        if not html: continue
        # 这里的判断就是判断get的返回值是否为None，如果是就是请求出错，需要跳过斜面的操作以免出现其他问题
        html = html.replace("\n", "").replace("\r", "").replace("\t", "").replace(" ", "")
        urls = findall(r'class="content__list--item--aside"target="_blank"href="/zufang(.*?)"title="', html)
        for u in urls:
            result.append(baseurl + u)
    return result


# 这个函数通过正则读出HTML中的信息，并写入文件
async def get_roommessage(html, bname, w2):
    '''
    无关紧要的正则提取和写文件操作
    '''


async def get_rooms(html, num, bname, w2):
    # 根据数量获取指定数量的房间urls
    if num < 1000:
        room_urls = await get_roomurls(html, num)
    else:
        room_urls = await get_roomurls(html, 1000)
    if not room_urls: return
    for u in room_urls:
        room_r = await get(u)  # 爬取每个房URL的HTML
        if not room_r:
            continue
        try:
            room_message = await get_roommessage(room_r, bname, w2)  # 筛选并写入每个房间的信息
        except:
            pass


async def geturls(block, bname):
    blockurl = baseurl + block
    block_r = await get(blockurl)
    sub_blocks = get_subblock(block_r)
    return sub_blocks


async def get_message_main(block, bname, w1, w2):
    print("运行了main一次")
    blockurl = baseurl + block  # 拼接成区域的完整URL
    block_r = await get(blockurl)  # 获取这个URL的HTML
    room_num = get_roomnum(block_r)  # 获取每个区域的房间数量
    w1.writerow([bname, room_num])  # 写入文件
    result = await get_rooms(block_r, int(room_num), bname, w2)  # 爬取每个区域的房间


async def main():
    global session  # 将session扩展为全局变量
    session = aiohttp.ClientSession()  # 初始化获得一个session

    # 创建文件，写入表头
    f1 = open('file1.csv', 'w', encoding='utf-8')
    f2 = open('file2.csv', 'w', encoding='utf-8')
    w1 = csv.writer(f1)
    w2 = csv.writer(f2)
    w1.writerow(['行政区域', '挂网租房数量'])

    # 获取每个区域的url
    base_r = await get(baseurl)
    block_urls = get_blockurls(base_r)

    # 创建并运行协程
    indextasks = [asyncio.ensure_future(get_message_main(block, bname, w1, w2)) for block, bname in
                  zip(block_urls, block_list)]
    result = await asyncio.gather(*indextasks)

    # 关闭文件和session
    f1.close()
    f2.close()
    await session.close()


def paicsv():
    data = []
    reader = csv.reader(open("file2.csv", "r"))
    for row in reader:
        data.append(row)
    data.sort()
    with open("file2.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            ['行政区域', '区域', '小区', '房型', '房源维护时间', '面积', '朝向', '维护', '入住', '楼层', '电梯', '车位', '用水', '用电', '燃气', '采暖', '租期',
             '看房', '付款方式', '租金', '押金', '洗衣机', '空调', '衣柜', '电视', '冰箱', '热水器', '床', '暖气', '宽带', '天然气'])
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    start = time.time()
    print("Start at: ", start)
    # 运行main函数
    asyncio.get_event_loop().run_until_complete(main())
    end = time.time()
    print("End at:   ", end)
    print("Time cost:", end - start)
    paicsv()
