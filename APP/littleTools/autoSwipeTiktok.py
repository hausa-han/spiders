# coding:utf-8
import threading

import uiautomator2 as u2
import time, datetime
from random import randint
from ..accounts.secretAccounts import tiktokAccounts
import os


class Phone:
    def __init__(self, deviceID, appName):
        self.deviceID = deviceID
        self.appName = appName

    def openAPP(self):
        self.driver = u2.connect_usb(deviceName)
        self.driver.app_stop(self.appName)
        self.driver.app_start(self.appName)

    def stopAPP(self):
        self.driver.app_stop(self.appName)

    def getSize(self):
        x = self.driver.window_size()[0]
        y = self.driver.window_size()[1]
        return x, y

    def swipeUp(self, t=0.05):
        l = self.getSize()
        x1 = int(l[0] * 0.5)  # x坐标
        y1 = int(l[1] * 0.75)  # 起始y坐标
        y2 = int(l[1] * 0.25)  # 终点y坐标
        self.driver.swipe(x1, y1, x1, y2, t)


def randLongSleep(text=''):
    sleepTime = randint(5,13)
    print('Random long sleep {}: {}'.format(sleepTime, text))
    time.sleep(sleepTime)

def randShortSleep(text=''):
    sleepTime = randint(1,3)
    print('Random short sleep {}: {}'.format(sleepTime, text))
    time.sleep(sleepTime)

def tiktokReLogin(deviceName, appName, account, key):
    # Re login to another account
    phone = Phone(deviceName, appName)
    phone.openAPP()
    randLongSleep('reLogin')
    print('ReLogin to {}'.format(account))
    randLongSleep('Click me')
    phone.driver.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/root_view"]/android.widget.FrameLayout[4]/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]').click()
    randShortSleep('Click 三')
    phone.driver(resourceId="com.ss.android.ugc.aweme.lite:id/f6c").click()
    randShortSleep('Click settings')
    phone.driver(text='设置').click()
    randShortSleep('Swipe up')
    phone.swipeUp()
    randShortSleep('Click logout')
    phone.driver(text='退出登录').click()
    randShortSleep('Click logout in pop-up')
    phone.driver(resourceId="android:id/button1").click()
    randShortSleep('Stop and reOpen APP')
    phone.stopAPP()
    phone.openAPP()
    randLongSleep('Click me')
    phone.driver.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/root_view"]/android.widget.FrameLayout[4]/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]').click()
    randShortSleep('Check if special')
    if not phone.driver(text='认证服务由中国移动提供').exists:
        print('Is special')
        phone.driver.click(0.589, 0.883)
    randShortSleep('Click circle')
    phone.driver(resourceId="com.ss.android.ugc.aweme.lite:id/jhu").click()
    randShortSleep('Click other phone login')
    phone.driver(text='其他手机号码登录').click()
    randShortSleep('Click key login')
    phone.driver(resourceId="com.ss.android.ugc.aweme.lite:id/frk").click()
    randShortSleep('Input phone number')
    phone.driver(resourceId="com.ss.android.ugc.aweme.lite:id/grx").click()
    randShortSleep('Do input')
    phone.driver(resourceId="com.ss.android.ugc.aweme.lite:id/grx").send_keys(account)
    randShortSleep('Input key')
    phone.driver(resourceId="com.ss.android.ugc.aweme.lite:id/gpc").click()
    randShortSleep('Do input')
    phone.driver(resourceId="com.ss.android.ugc.aweme.lite:id/gpc").send_keys(key)
    randShortSleep('Click circle')
    phone.driver(resourceId="com.ss.android.ugc.aweme.lite:id/jhu").click()
    randShortSleep('Click login')
    phone.driver(resourceId="com.ss.android.ugc.aweme.lite:id/login").click()
    randShortSleep('Waiting login 01')
    randShortSleep('Waiting login 02')
    phone.driver.click(0.589, 0.883)
    phone.stopAPP()


def tiktokDoSwipe(deviceName, appName):
    phone = Phone(deviceName, appName)
    phone.openAPP()
    for i in range(0, 1):
        randLongSleep('Swipe wait')
        if phone.driver(text='继续看视频赚钱').exists:
            phone.driver(text='继续看视频赚钱').click()
            print('Clicked \'继续看视频赚钱\'')
        if phone.driver(text='广告').exists:
            randLongSleep('Sleep more time at advertisement')
        phone.swipeUp()
    print('Finished a account')

def startTiktokSwipe(deviceName, appName, tiktokAccounts):
    for key, value in tiktokAccounts.items():
        tiktokDoSwipe(deviceName, appName)
        tiktokReLogin(deviceName, appName, key, value)


if __name__ == "__main__":
    # Config
    deviceName = '9a9abd39'  # mobil device name: adb devices
    appName = "com.ss.android.ugc.aweme.lite"  # app package name: adb shell dumpsys window | grep mCurrentFocus

    # Accounts
    tiktokAccounts = dict.copy(tiktokAccounts)

    # start
    while True:
        startTiktokSwipe(deviceName, appName, tiktokAccounts)


