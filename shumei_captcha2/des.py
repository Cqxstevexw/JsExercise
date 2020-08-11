# -*- coding：utf-8 -*-

import base64

from Crypto.Cipher import DES


def encrypt(key, text):
    encrypter = DES.new(key.encode(), DES.MODE_ECB)
    length = 8
    count = len(text)
    if count < length:
        add = (length - count)
        text = text + ('\0' * add)
    elif count > length:
        add = (length - (count % length))
        text = text + ('\0' * add)
    ciphertext = encrypter.encrypt(text.encode())
    return base64.b64encode(ciphertext)


def decrypt(key, text):
    decrypter = DES.new(key.encode(), DES.MODE_ECB)
    return decrypter.decrypt(text).decode()


if __name__ == '__main__':
    print(encrypt('f3c2b92a', 'zh-cn'))
    print(encrypt('f3c2b92a', 'default'))
    print(encrypt('f3c2b92a', '0'))
    print(encrypt('f3c2b92a', '1'))
    print(encrypt('f3c2b92a', '0.225'))
    print(encrypt('f3c2b92a', '200'))
    print(encrypt('f3c2b92a', '400'))
    print(encrypt('f3c2b92a', '-1'))
    print(encrypt('f3c2b92a', '[(0,0,0),(90,-1,152)]'))
    print(encrypt('f3c2b92a', str([(0, 0, 0), (90, -1, 152)])))
    print(decrypt('f3c2b92a', base64.b64decode(b'zFFKMtjhtAA=')))
    print([decrypt('f3c2b92a', base64.b64decode(b'sDGPWqptPHUpR59eGNR+6lvjw65vPPrO'))])

    print(encrypt("8548c4c7", '0.155'))
    print(encrypt("8548c4c7", '[[0, 11, 0],[35, -1, 100],[51, -1, 200],[62, 2, 300]]'))
    print(encrypt("8548c4c7", "[[0,11,0],[35,-1,100],[51,-1,200],[62,2,300]]"))
