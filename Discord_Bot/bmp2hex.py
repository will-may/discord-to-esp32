from PIL import Image
import os

def clamp(x):
        return max(0, min(x, 255))

def bmptohex():
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
    f = open("image2" + ".h", "w+")

    for y in range(0, im.size[1]):
       for x in range(0, im.size[0]):
            r, g, b = pix[x][y]
            var = "0x{0:02x}{1:02x}{2:02x}".format(clamp(b), clamp(g), clamp(r))
            f.write("%s," % var)
    f.close()
    print("whahhs")