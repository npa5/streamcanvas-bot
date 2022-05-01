from PIL import Image
import canvas.log as log

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def load(name):
    try:
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
        return image
    except:
        log.error("Image not found, make sure you specified the right image in the config file.")

def size(name):
    img = Image.open(name, 'r')
    return [img.width, img.height]