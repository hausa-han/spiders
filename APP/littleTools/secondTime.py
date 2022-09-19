import time

times = 0
startTime = time.time()
while True:
    nowTime = time.time()
    if int(nowTime-startTime) > times:
        times += 1
        print(times)