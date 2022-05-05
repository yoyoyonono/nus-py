import urllib.request
import struct

URL_BASE = 'http://ccs.cdn.wup.shop.nintendo.net/ccs/download'

def parseTMD(tmd: bytes):
    TitleID = struct.unpack('>q', tmd[0x18C:0x194])[0]
    content_ids = []
    for i in range(0xB04, 0xB04+36*struct.unpack('>h', tmd[0x1DE:0x1E0])[0], 36):
        content_ids.append(struct.unpack('>I', tmd[i:i+4])[0])
    return content_ids

def getNUScontentID(titleID):
    return parseTMD(downloadTMDtoByteArray(titleID, 0))[0]

def downloadTMDtoByteArray(titleID: int, version: int):
    if version > 0:
        version_suf = f'.{version}'
    else:
        version_suf = ''
    url = URL_BASE + '/' + hex(titleID)[2:].rjust(16, '0') + '/tmd' + version_suf
    return urllib.request.urlopen(url).read()

def downloadAndDecrypt(titleID: int):
    url = URL_BASE + '/' + hex(titleID)[2:] + '/' + oct(getNUScontentID())[2:]

if __name__ == "__main__":
    ids = (parseTMD(downloadTMDtoByteArray(0x00050000101b0700, 0)))
    for x in ids:
        print(hex(x)[2:].rjust(8,'0'))