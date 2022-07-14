import random
import operator

def randomData(size):
    data = []
    for x in range(size):
        data.append(random.randrange(0,255))
    return data

def displayData(data):
    print("-"*20)
    for index, item in enumerate(data, start=1):
        print(f'{index} = {item} ({hex(item)})')
    print("-"*20) 

def writeBytes(filename, bytes):
    with open(filename,'wb') as file:
        for i in bytes:
            file.write(i.to_bytes(1, byteorder='big'))

def readBytes(filename):
    bytes = []
    with open(filename,'rb') as file:
        while True:
            b = file.read(1)
            if not b:
                break
            bytes.append(int.from_bytes(b, byteorder='big'))
    return bytes

if __name__ == '__main__':
    outbytes = randomData(10)
    displayData(outbytes)

    filename = 'test.dat'
    writeBytes(filename,outbytes)

    inbytes = readBytes(filename)
    displayData(inbytes)
    print(f'Match: {operator.eq(outbytes,inbytes)}')
