from utils.base64 import encode

if __name__ == '__main__':
    while True:
        print('Input string to base64 encode:')
        s = input()
        print(encode(s), end='\n\n')
