import zipfile, io, requests, base64

pillow_supported = [".bmp",".dib",".dcx",".eps",".ps",".gif",".icns",
                        ".ico",".im",".jpg",".jpeg",".jpe",".j2k",".j2p",
                        ".jp2",".jpc",".jpf",".jpx",".mpo",".msp",".pcx",
                        ".png",".ppm",".pbm",".pgm",".psd",".sgi",".tiff",
                        ".tif",".webp",".xbm",".xpm"]

def uploaded_content_handler(contents, filename):
    content_type, content_string = contents.split(',')
    decoded_content = base64.b64decode(content_string)
    if filename.endswith('.zip'):
        pass

# unzips in memory
def unzip(decoded_content_that_is_zip):
    file_list = None
    with zipfile.ZipFile(io.BytesIO(decoded_content_that_is_zip)) as z:
        file_list = z.namelist()
    return file_list
        


# validate that the file is supported
# file_list has to be processed by this fn
def file_is_supported(filename, extensions=pillow_supported):
    # returns True for any item in iterable (of any(y))
    # else, iterable empty, False
    return any(filename.lower().endswith(ext) for ext in extensions)

# returns only those files in zip that are supported
def processable_items(file_list):
    items_to_process = []
    for image_filename in file_list:
        if file_is_supported(image_filename):
            items_to_process.append(image_filename)
    return items_to_process
        


# # given the dimensions selected, 
# def user_dims_selection():
#     pass

# def hash_picture():
#     pass

