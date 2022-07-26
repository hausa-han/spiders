import requests
import base64
import codecs
import json
import os
import random
from time import sleep
from Crypto.Cipher import AES

#The Spider
class Spider():
    def __init__(self):
        self.header = {
                'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
                'Referer': 'http://music.163.com/'
                }
        self.baseurl='https://music.163.com/'

    #Use the API to get the ID of the song the user searches for
    def get_song_ID(self, songname):
        url = 'http://music.163.com/api/search/pc'
        data = {
                's':songname,
                'offset':0,
                'limit':1,
                'type':1
                }
        jsondata = requests.post(url, data=data)
        songmessage = json.loads(jsondata.text)
        songID = songmessage['result']['songs'][0]['id']
        return str(songID)

        


    #Get song hotComments and return as a list
    def getcomments(self, songID):
        print("Reading Comments......\n")
        url = self.baseurl + 'weapi/v1/resource/comments/R_SO_4_' + songID + '?csrf_token='
        data = Data_of_Comments(songID)
        text = data.make_random_string()
        params = data.get_params(text)
        encSecKey = data.get_encSecKey(text)
        senddata = {
                'params':params,
                'encSecKey':encSecKey
                }
        jsondata = requests.post(url, data=senddata, headers=self.header)
        #print(jsondata.text)
        users = json.loads(jsondata.text)
        comments = []
        for user in users['hotComments']:
            userdic = {
                    'nickname':user['user']['nickname'],
                    'content':user['content'],
                    'liked':user['likedCount']
                    }
            comments.append(userdic)
        return comments

    #Show the hotComments
    def show(self, comments):
        for comment in comments:
            print('\nnickname:\n'+comment['nickname']+'\ncomment:\n'+comment['content']+'\nliked')
            print(comment['liked'])
            sleep(len(comment['content']) * 0.1)

    def run(self):
        songname = input("Input a song name:")
        songID = self.get_song_ID(songname)
        comments = self.getcomments(songID)
        self.show(comments)


#Imitate the enctyption process of JS script, to get the POST data
class Data_of_Comments():
    def __init__(self, songID):
        self.params = ''
        self.encSecKey = ''
        self.songID = songID
        self.second_param = '010001'
        self.third_param = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.fourth_param = '0CoJUm6Qyw8W8jud'

    #Randomly generate a string of length 16
    def make_random_string(self):
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(16)))))[0:16]

    def aesEncrypt(self, data, key):
        vi = '0102030405060708'
        pad = lambda s: s + (16 - len(s)%16) * chr(16 - len(s)%16)
        data = pad(data)
        cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
        encryptedbytes = cipher.encrypt(data.encode('utf8'))
        encodestrs = base64.b64encode(encryptedbytes)
        enctext = encodestrs.decode('utf8')
        return enctext

    #Get the params
    def get_params(self, text):
        self.first_param = '{rid: "R_SO_4_' + self.songID + '", offset: "0", total: "true", limit: "20", csrf_token: ""}'
        self.params = self.aesEncrypt(self.first_param, self.fourth_param)
        self.params = self.aesEncrypt(self.params, text)
        return self.params

    def rsaEncrypt(self, pubKey, text, modulus):
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    #Get the encSecKey
    def get_encSecKey(self,text):
        pubKey = self.second_param
        moudulus = self.third_param
        self.encSecKey = self.rsaEncrypt(pubKey, text, moudulus)
        return self.encSecKey

#Main func
def main():
    spider = Spider()
    spider.run()

#Just Run It!
if __name__ == '__main__':
    main()
