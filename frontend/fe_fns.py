import zipfile, io, requests, base64, os
from dash import html

pillow_supported = [".bmp",".dib",".dcx",".eps",".ps",".gif",".icns",
                        ".ico",".im",".jpg",".jpeg",".jpe",".j2k",".j2p",
                        ".jp2",".jpc",".jpf",".jpx",".mpo",".msp",".pcx",
                        ".png",".ppm",".pbm",".pgm",".psd",".sgi",".tiff",
                        ".tif",".webp",".xbm",".xpm"]

# returns decoded contents and its filename in a tuple
def uploaded_content_handler(contents, filename):
    content_type, content_string = contents.split(',')
    decoded_content = base64.b64decode(content_string)
    return decoded_content, filename

# unzips in memory
def unzip(decoded_content_that_is_zip):
    file_list = None
    with zipfile.ZipFile(io.BytesIO(decoded_content_that_is_zip)) as z:
        file_list = z.namelist()
    return file_list
        
# extracts to a provisional dir
def extract_zip_to_disk(decoded_content_that_is_zip):
    provisional_dir = '/storimages'
    provisional_dir_exists = os.path.exists(provisional_dir)
    
    if provisional_dir_exists:
        print('prov exists')
        os.rmdir(provisional_dir)
    elif not provisional_dir_exists:
        print('prov not exists')
        os.makedirs(provisional_dir)

    with zipfile.ZipFile(io.BytesIO(decoded_content_that_is_zip)) as z:
        z.extractall(provisional_dir)

# saves the picture uploaded
def save_uploaded_picture(decoded_contents, filename):
    uploaded_picture_path = os.path.join('/storimages',filename)
    
    if os.path.exists(uploaded_picture_path):
        os.remove(uploaded_picture_path)
    
    with open(uploaded_picture_path, 'wb') as f:
        f.write(decoded_contents)
    
    return uploaded_picture_path

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

# will return a list of files to show to the user before unblocking the submit 
# button
def show_items(filename_or_list):
    if isinstance(filename_or_list, list):
        show_items = html.Div([
        html.H3("Processable items"),
        html.Ul([html.Li(filename) for filename in filename_or_list], id="list-container")])
        return show_items
    elif isinstance(filename_or_list, str):
        show_items = html.Div([
        html.H3("Processable items"),
        html.Ul([html.Li(filename_or_list)], id="list-container")])
        return show_items

def resize_to_array(dimensions_selected):
    choices = {
        'Photo galleries = 120x90':[120, 90],
        'Video = 160x120':[160, 120],
        'Social media profile picture = 100x100':[100, 100],
        'Online store - small = 80x80':[80, 80],
        'Online store - large = 150x150':[150, 150],
        'Icons = 96x96':[96, 96]
    }
    dimensions_array = choices[dimensions_selected]
    return dimensions_array
