# Caesar
s = 'ZpyLfxGmelDeftewJwFbwDGssZszbliileadaa'
for i in range(0,114515):
    t = ''
    I = i
    print(I)
    for c in s:
        if 'a' <= c <= 'z':
            t += chr( ord('a') + (ord(c) - ord('a') + I) %26)
        elif 'A' <= c <= 'Z':
            t += chr( ord('a') + (ord(c) - ord('A') + I) %26)
        else:
            t += c
        I = I + 114514
    print(t)
