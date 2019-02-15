import os, sys
from PIL import Image
from getopt import getopt



#https://pillow.readthedocs.io/en/3.1.x/reference/PixelAccess.html
def encode(file_name, image):
    px_mask = 12
    ch_mask = 3
    i, j = [0, 0]
    n, m = image.size
    pixels = image.load()

    with open(file_name, 'r') as fi:
        path = os.path.realpath(fi.name)
        file_size = os.path.getsize(path)
        print('file size:', file_size)
        #TODO: add file size in the first byte, then add in a byte each
        for k in range(0, 4):
                    px = list(pixels[i,j])
                    px[2] = px[2] & px_mask
                    px[2] = px[2] | (file_size & ch_mask)
                    pixels[i,j] = tuple(px)
                    file_size = file_size >> 2
                    j = j + 1 if j + 1 < m else 0
                    i = i + 1 if j == 0 else i

        for line in fi:
            for char in line:
                num = ord(char)
                for k in range(0, 4):
                    px = list(pixels[i,j])
                    px[2] = px[2] & px_mask
                    px[2] = px[2] | (num & ch_mask)
                    pixels[i,j] = tuple(px)
                    num = num >> 2
                    j = j + 1 if j + 1 < m else 0
                    i = i + 1 if j == 0 else i
    

def decode(image_name):
    res = ""
    image = Image.open(image_name)
    ch_mask = 3
    i, j = [0, 0]
    n, m = image.size
    pixels = image.load()
    file_size = 0
    val = 0
    for k in range(0, 4):
        px = list(pixels[i,j])
        nb = px[2] & ch_mask
        file_size += nb * (4 ** k)
        
        j = j + 1 if j + 1 < m else 0
        i = i + 1 if j == 0 else i

    while file_size > 0:
        char = 0
        for k in range(0, 4):
            px = list(pixels[i,j])
            nb = px[2] & ch_mask
            char += nb * (4 ** k)
            
            j = j + 1 if j + 1 < m else 0
            i = i + 1 if j == 0 else i
        file_size -= 1
        res += chr(char) 
    print(res)


def samePic(px1, px2):
    for i in range(0, 8):
        for j in range(0, 8):
            if px1[i,j] != px2[i,j]:
                return False
    return True




def main():
    #get arguments
    options, args = getopt(sys.argv[1:], "i:f:s:d")
    im = None
    file_name = None
    decode = False
    usage = 'python3 steg.py -i image name/path -f message file/path -s message as string'

    for o, a  in options:
        if o == '-i':
            image_type = a.split('.')
            im = Image.open(a)
            if image_type[1] == 'jpg':
                lossless = image_type[0] + '.png'
                im.save(lossless)
                im = Image.open(lossless)
            
        elif o == '-f':
            file_name = a
        elif o == '-s':
            with open('steg_msg.txt', 'w') as fi:
                fi.write(a)
                file_name = 'steg_msg.txt'
        elif o == '-d':
            decode = True
        else:
            print('<usage>:', usage)
            return
    
    if im and file_name:
        encode(file_name, im)
        im.save('steg.png')
        os.remove(file_name)

    if decode:
        decode('steg.png')

    # im = Image.open('bevo.jpg')
    # im.save('bevo.png')
    # im2 = Image.open('bevo.png')
    # encode('msg.txt', im2)
    # im2.save('steg.png')
    # decode('steg.png')
    

main()