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
    split_path = os.path.split(filename) # [directory, filename]
    dimensions = str(dimensions_tuple[0]) + '_x_' +  str(dimensions_tuple[1])
    head = split_path[0]
    tail = split_path[1]
    name, extension = tail.split('.') # tail.split() = ['cats', 'jpeg']
    new_filename = os.path.join(head, f'{name}_{dimensions}.{extension}')
    return new_filename

# supposedly, to this point, only supported pics made it here
# but one never knows... really!
# dimensions = tuple of (width, height)
def resize_image(filename, dimensions_tuple):
    with Image.open(filename) as img:
        img = img.resize(dimensions_tuple, Image.ANTIALIAS)
        thumbnail_path = generate_filename_tn(filename, dimensions_tuple)

        # add try-excepts outside, to the most general case for now
        img.save(thumbnail_path)
