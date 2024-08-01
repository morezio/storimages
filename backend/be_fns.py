import os 
from PIL import Image


# tn = thumbnail
# outputs the filename to store a thumbnail
# head to toe in the app, dimensions are always numbers;
def generate_filename_tn(filename, dimensions_tuple): 
    # recall that filename is an abs path both ends can access
    # so the tail is the name of the image
    # PATH MUST BE NORMALIZED (single dot, no spaces, lower, no escaping chars)
    # this is one of the reasons why the hashing made sense originally; we
    # catch with that later on
    strip_ext = filename.split('.') # (path, jpeg)
    extension = strip_ext[1]
    dimensions = str(dimensions_tuple[0]) + 'x' +  str(dimensions_tuple[1])
    # /home/cats_10x10.jpeg
    suffix = f'_{dimensions}.{extension}'
    new_filename = strip_ext[0]+suffix
    return new_filename

# supposedly, to this point, only supported pics made it here
# yet, handle the exceptions higher for now
# dimensions = tuple of (width, height); must be numerical all the way
def resize_image(filename, dimensions_tuple):
    with Image.open(filename) as img:
        img = img.resize(dimensions_tuple, Image.ANTIALIAS)
        thumbnail_path = generate_filename_tn(filename, dimensions_tuple)
        # add try-excepts outside, to the most general case for now
        img.save(thumbnail_path)
        return thumbnail_path
