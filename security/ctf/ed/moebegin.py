s = 'tv|zmbA)kF(jFj)Fpwm*k*jmpw~88888d'

for i in range(0, len(s)):
    print(chr(ord(s[i]) ^ 0x19), end='')

print()
s = 97
print(chr(s))