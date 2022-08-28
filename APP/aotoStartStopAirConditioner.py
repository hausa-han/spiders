# coding:utf-8
import threading

import uiautomator2 as u2
import time, datetime
from random import randint
import os


class Phone:
    def __init__(self, deviceID, appName):
        self.deviceID = deviceID
        self.appName = appName

    def openAPP(self):
        self.driver = u2.connect_usb(self.deviceID)
        self.driver.app_stop(self.appName)
        self.driver.app_start(self.appName)

    def closeAPP(self):
        self.driver.app_stop(self.appName)



def airConditionerPowerAction(action):
    phone = Phone(deviceName, appName)
    phone.openAPP()
    time.sleep(3)
    phone.driver(text='格力空调').click()
    time.sleep(2)
    phone.driver(resourceId="com.duokan.phone.remotecontroller:id/ac_command_power").click()
    if action == 'Power off':
        time.sleep(1)
        phone.driver(resourceId="com.duokan.phone.remotecontroller:id/ac_command_power").click()
    time.sleep(3)
    phone.closeAPP()
    time.sleep(1)
    print('[{}]: {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), action))



if __name__ == '__main__':
    # Config
    deviceName = '331f3b9'  # mobil device name: adb devices
    appName = "com.duokan.phone.remotecontroller"  # app package name: adb shell dumpsys window | grep mCurrentFocus

    times = 0

    while True:
        airConditionerPowerAction('Power on')
        time.sleep(3600)
        airConditionerPowerAction('Power off')
        time.sleep(3600)
        times += 1
        print('Loop {} times'.format(times))
