from PIL import Image
import canvas.log as log

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def load(name):
        image = []
        img = Image.open(name, 'r')
        width, height = img.size
        pixels = list(img.getdata()) # Reads every pixel from the image
        
        for pixel in pixels: 
            cl = ()
            for i in range(0,3):
                cl = cl + (pixel[i],)
            image.append(rgb_to_hex(cl)) # Converts all pixels from rgb to hex and
                                         # appends them to a list.
        log.info("Successfully loaded image.")
        img2d = to2d(image, width, height) # Converts 1 dimensional to 2 dimenional array,
        return img2d                       #this makes using the array later on much easier.
  
def to2d(array, width, height):
    array2 = []
    for i in range(0,height):
        array2.append([])
        for n in range(0+i*width,(0+i*width)+width):
            array2[i].append(array[n])
    return array2
