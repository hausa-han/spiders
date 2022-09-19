# coding:utf-8
import threading

import uiautomator2 as u2
import time, datetime
from random import randint
from APP.accounts.secretAccounts import iLoveKeDaAccounts

import os

def log(s):
    print('[{}]: {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), s))


class Phone:
    def __init__(self, deviceName, appName):
        self.deviceName = deviceName
        self.appName = appName
        self.d = u2.connect_usb(deviceName)  # connect to mobile

    def doTest(self):
        self.d.app_stop_all()
        self.d.app_start(self.appName)
        self.wait('微信')

    def wait(self, s):
        times = 0
        maxWaitTime = 10
        while not self.d(text=s).exists:
            time.sleep(1)
            times += 1
            if times > maxWaitTime:
                log('There might be something wrong, restarting now......')
                self.doTest()
        time.sleep(1)


if __name__ == '__main__':
    # Config
    deviceID = '9a9abd39'  # mobil device name: adb devices
    appID = 'com.tencent.mm'  # app package name: adb shell dumpsys window | grep/findstr mCurrentFocus

    phone = Phone(deviceID, appID)
    phone.doTest()