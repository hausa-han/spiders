# coding:utf-8
import threading

import uiautomator2 as u2
import time, datetime
from random import randint
from APP.accounts.secretAccounts import iLoveKeDaAccounts

import os


class Phone:
    def __init__(self, deviceID, iLoveKeDaAppName, fakeLocationAppName):
        self.deviceID = deviceID
        self.iLoveKedaAppName = iLoveKeDaAppName
        self.fakeLocationAppName = fakeLocationAppName

    def startFakeLocation(self):
        self.driver = u2.connect_usb(self.deviceID)
        print('[{}]: '.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), end='')
        print('Starting FakeLocation...')
        self.driver.app_stop(self.fakeLocationAppName)
        self.driver.app_start(self.fakeLocationAppName)
        print('[{}]: '.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), end='')
        print('Fake Location Started')

        time.sleep(1)
        self.driver(resourceId="com.lerist.fakelocation:id/f_fakeloc_tv_service_switch").click()
        print('[{}]: '.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), end='')
        print('Location Modify Started')

        time.sleep(1)
        self.driver(resourceId="com.lerist.fakelocation:id/i_loc_history_tv_name").click()
        print('[{}]: '.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), end='')
        print('Location Modified to \"郑州市生龙世纪花园三区\"')
        time.sleep(1)

        self.driver(resourceId="com.android.systemui:id/center_group").click()
        print('[{}]: '.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), end='')
        print('Switched to Android desktop')


    def doReportSafety(self, studentId, passwd):
        self.driver.app_stop(self.iLoveKedaAppName)
        self.driver(text="我i科大").click()
        print('[{}]: '.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), end='')
        print('Changing account to: {}:{}.'.format(studentId, passwd))

        while not self.driver(resourceId="com.lantu.MobileCampus.haust:id/agreeBtn").exists:
            time.sleep(1)
            if self.driver(text='报平安').exists:
                self.logout()
                time.sleep(1)
                self.driver(text="我i科大").click()
        self.driver.xpath('//*[@resource-id="com.lantu.MobileCampus.haust:id/passwordLoginLayout"]/android.widget.RelativeLayout[1]').set_text(studentId)
        time.sleep(1)
        self.driver(resourceId="com.lantu.MobileCampus.haust:id/passwordTxt").set_text(passwd)
        time.sleep(1)
        self.driver(resourceId="com.lantu.MobileCampus.haust:id/loginBt").click()
        time.sleep(1)
        self.driver(resourceId="com.lantu.MobileCampus.haust:id/agreeBtn").click()
        time.sleep(1)
        self.driver(resourceId="com.lantu.MobileCampus.haust:id/loginBt").click()
        time.sleep(1)

        while not self.driver(text='报平安').exists:
            time.sleep(1)
        print('[{}]: '.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), end='')
        print('Login success')

        print('[{}]: '.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), end='')
        print('Reporting safety.')
        self.driver(text='报平安').click()
        while not self.driver(text='获取').exists:
            time.sleep(1)
        print('[{}]: '.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), end='')
        print('Getting location')
        self.driver(text='获取').click()
        time.sleep(2)

        while self.driver(text='行程登记').exists:
            time.sleep(1)
            self.driver(text='刷新').click()
            time.sleep(2)
            if self.driver(text='行程登记').exists:
                self.startFakeLocation()
                self.driver(text="我i科大").click()
                time.sleep(2)
        self.swipeUp()
        self.driver(text='确定数据填写真实、有效').click()
        self.driver(text='提交').click()
        time.sleep(3)
        print('[{}]: '.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), end='')
        print('Report success: {}\n'.format(studentId))
        time.sleep(2)

        self.logout()


    def logout(self):
        print('[{}]: '.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), end='')
        print('Logout now.')
        self.driver.app_stop(iLoveKeDaAppName)
        self.driver.app_start(iLoveKeDaAppName)
        time.sleep(3)
        self.driver.click(0.93, 0.916)
        while not self.driver(text='一卡通余额').exists:
            time.sleep(1)
            self.driver.click(0.93, 0.916)
        self.driver(text='设置').click()
        self.driver.click(0.512, 0.252)
        time.sleep(2)
        while not self.driver.xpath('//*[@resource-id="com.lantu.MobileCampus.haust:id/passwordLoginLayout"]/android.widget.RelativeLayout[1]').exists:
            self.driver.click(0.512, 0.252)
            time.sleep(2)
        self.driver.app_stop(iLoveKeDaAppName)

    def screenShot(self):
        screenshot_name = '{}//{}'.format(currentPath,screenShotStoragePath) + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
        self.driver.screenshot(screenshot_name)

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


if __name__ == '__main__':
    # Config
    deviceName = '9a9abd39'  # mobil device name: adb devices
    fakeLocationAppName = "com.lerist.fakelocation"  # app package name: adb shell dumpsys window | grep mCurrentFocus
    iLoveKeDaAppName = "com.lantu.MobileCampus.haust"

    accounts = dict.copy(iLoveKeDaAccounts)

    screenShotStoragePath = 'reportSafetyResult'

    # Result will save here
    currentPath = os.getcwd()
    if not os.path.exists('./{}'.format(screenShotStoragePath)):
        os.makedirs(currentPath + "/{}".format(screenShotStoragePath))

    phone = Phone(deviceName, iLoveKeDaAppName, fakeLocationAppName)


    unComplete = dict.copy(accounts)

    while unComplete != {}:
        accounts = dict.copy(unComplete)
        for account,key in accounts.items():
            try:
                phone.startFakeLocation()
                phone.doReportSafety(account, key)
                unComplete.pop(account)
                phone.driver.app_stop_all()
            except Exception as e:
                print('Account {} fail, try again after all.'.format(account))
                continue

