import os
from PIL import Image
import struct

def clamp(x):
        return max(0, min(x, 1))

def bmptobytes():
    try:
      os.remove("image2.h")
    except:
      print("all clean")
    im = Image.open('image.bmp')
    rows, cols = (im.width, im.height)
    pix = [[(0,0,0) for i in range(cols)] for j in range(rows)]
    for x in range(im.width):
        for y in range(im.height):
            #print(x, y)
            pix[x][y]= im.getpixel((x, y))
            #print(im.getpixel((x, y)))

    f = open("image2" + ".h", "wb")
    # you could actually cram two pixels into each byte, which would be a lot more efficient,
    # but I just haven't added that yet.
    for y in range(0, im.size[1]):
       for x in range(0, im.size[0]):

                r, g, b = pix[x][y]
                byte_send = clamp(r) + (clamp(g)*2) + (clamp(b)*4)
                r1 = struct.pack('<B', byte_send)
                f.write(r1)
    f.close()
    print("whahhs")