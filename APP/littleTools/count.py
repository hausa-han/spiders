import datetime


i = 0
log = ''
while True:
    s = input()
    i += 1
    print('{}: Count: {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), i))
    if s == 'q':
        print('\n\nlog here:\n\n{}'.format(log))
        break
    if s != '':
        log = log + '{}: {}\n'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), s)
