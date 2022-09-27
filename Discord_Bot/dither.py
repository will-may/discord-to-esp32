import numpy as np
from PIL import Image
import os

new_height = 0
new_width = 0

def start_dithering(name):
    print("Commencing Dither!")
    global new_height, new_width
    img_name = name
    # Read in the image, convert to greyscale.
    img = Image.open(img_name)
    width, height = img.size
    new_width = 300
    new_height = int(height * new_width / width)
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    nc = 2
    print('nc =', nc)
    dim = fs_dither(img, nc)
    dim.save('dithered-{}.png'.format(nc))

def get_new_val(old_val, nc):
    return np.round(old_val * (nc)) / (nc)

# For RGB images, the following might give better colour-matching.
#p = np.linspace(0, 1, nc)
#p = np.array(list(product(p,p,p)))
#def get_new_val(old_val):
#    idx = np.argmin(np.sum((old_val[None,:] - p)**2, axis=1))
#    return p[idx]

def fs_dither(img, nc):
    global new_height, new_width
    """
    Floyd-Steinberg dither the image img into a palette with nc colours per
    channel.

    """

    arr = np.array(img, dtype=float) / 255

    for ir in range(new_height):
        for ic in range(new_width):
            # NB need to copy here for RGB arrays otherwise err will be (0,0,0)!
            old_val = arr[ir, ic].copy()
            new_val = get_new_val(old_val, nc - 1)
            arr[ir, ic] = new_val
            err = old_val - new_val
            # In this simple example, we will just ignore the border pixels.
            if ic < new_width - 1:
                arr[ir, ic+1] += err * 7/16
            if ir < new_height - 1:
                if ic > 0:
                    arr[ir+1, ic-1] += err * 3/16
                arr[ir+1, ic] += err * 5/16
                if ic < new_width - 1:
                    arr[ir+1, ic+1] += err / 16

    carr = np.array(arr/np.max(arr, axis=(0,1)) * 255, dtype=np.uint8)
    return Image.fromarray(carr)
