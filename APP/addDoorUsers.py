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
    def __init__(self, deviceName, appName, pluginName, now):
        self.deviceName = deviceName
        self.appName = appName
        self.pluginName = pluginName
        self.nowCount = now
        self.d = u2.connect_usb(deviceName)
        self.d.app_start(appName)

    def startApp(self):
        self.stopAllApp()
        log('Starting {}'.format(self.appName))
        self.d(text=self.appName).click()
        log('{} started.'.format(self.appName))
        time.sleep(3)

    def stopAllApp(self):
        log('Stopping all APP.')
        self.d(resourceId="com.android.systemui:id/center_group").click()
        self.d(resourceId="com.android.systemui:id/recent_apps").click()
        self.d(resourceId="com.android.launcher:id/btn_clear").click()
        time.sleep(1)
        log('All APP stopped')

    def getSize(self):
        x = self.d.window_size()[0]
        y = self.d.window_size()[1]
        return x, y

    def swipeUp(self, t=0.05):
        l = self.getSize()
        x1 = int(l[0] * 0.5)  # x坐标
        y1 = int(l[1] * 0.75)  # 起始y坐标
        y2 = int(l[1] * 0.25)  # 终点y坐标
        self.d.swipe(x1, y1, x1, y2, t)

    def wait(self, s):
        times = 0
        while not self.d(text=s).exists:
            time.sleep(1)
            times += 1
            if times > 10:
                log('There might be something wrong, restarting now......')
                self.doTest(45)
        time.sleep(1)

    def doTest(self, n):
        self.startApp()
        log('Into {}.'.format(self.pluginName))
        self.d(text=self.pluginName).click()
        while not self.d(text='智能门日志').exists:
            time.sleep(1)
            self.d(text=self.pluginName).click()
        time.sleep(2)
        log('Swiping up.')
        self.swipeUp()
        while not self.d(text='用户管理').exists:
            self.swipeUp()
            time.sleep(1)
        time.sleep(1)
        log('Into 用户管理')
        self.d(text='用户管理').click()
        for i in range(self.nowCount, n):
            log('Adding NO.{} user.'.format(i))
            self.d.click(0.85,0.85)
            self.d(text='普通用户').click()
            self.wait('NFC门卡')
            log('Into password adding.')
            self.d.xpath('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup[7]/android.view.ViewGroup[1]/android.view.View[1]/android.widget.TextView[1]').click()
            self.wait('下一步')
            self.d.xpath('//android.widget.EditText').set_text(passwordList[i])
            self.d(text='下一步').click()
            time.sleep(1)
            self.d.xpath('//android.widget.EditText').set_text(passwordList[i])
            self.d(text='下一步').click()
            self.wait('完成')
            self.d(text='完成').click()
            self.wait('NFC门卡')
            self.d(resourceId="com.android.systemui:id/back").click()
            self.wait('用户管理')
            log('Add successfully\n')
            time.sleep(1)
            self.nowCount += 1

    def addPassword(self, n):
        for i in range(self.nowCount,n):
            self.swipeUp()
            self.swipeUp()
            self.swipeUp()
            log('Waiting 添加')
            self.d(text='添加')[-2].click()
            self.wait('下一步')
            self.d.xpath('//android.widget.EditText').set_text(passwordList[i])
            self.d(text='下一步').click()
            time.sleep(1)
            self.d.xpath('//android.widget.EditText').set_text(passwordList[i])
            self.d(text='下一步').click()
            self.wait('完成')
            self.d(text='完成').click()
            self.wait('NFC门卡')
            self.nowCount += 1
            time.sleep(1)


if __name__ == '__main__':
    # Config
    deviceID = '9a9abd39'  # mobil device name: adb devices
    appID = "米家"  # app package name: adb shell dumpsys window | grep mCurrentFocus
    pluginID = "云鹿智能门Y"
    added = 90

    passwordList = []

    for i in range(134567, 135000):
        passwordList.append(str(i))

    phone = Phone(deviceID, appID, pluginID, added)

    # phone.doTest(45)
    phone.addPassword(200)

    time.sleep(10)