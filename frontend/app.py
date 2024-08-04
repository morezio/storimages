import diskcache, flask, requests, os, shutil
from dash import DiskcacheManager, Dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from components import (storimages_layout, submit_button, preset_dimensions,
                        error_markdown)
from fe_fns import (uploaded_content_handler, file_is_supported, 
                    processable_items, unzip, show_items, extract_zip_to_disk,
                    save_uploaded_picture, resize_to_array, generate_payload,
                    load_picture_as_b, compress_into_zip,load_zip_as_b)

# POST endpoint
try:
    endpoint = os.environ['endpoint']
except KeyError:
    endpoint = 'http://be:80/create_thumbnail'

# app.py = essentially the app you interact with
# I move layout to another file to make it easier to follow

shared_path = '/storimages/data'
shared_path_exists = os.path.exists(shared_path)
if not shared_path_exists:
    os.mkdir(shared_path)

# dash works with callback functions that give the interactivity
# there's more to explain but the disk cache is needed. didn't go the
# traditional / recommended route because complexity grows and rn the route 
# isn't worth it right now
# 4 mins, 8gb, 8 shards
cache = diskcache.FanoutCache("./cache", shard=8, timeout=240, 
                              size_limit=80000000000)
lc_manager = DiskcacheManager(cache)

server = flask.Flask(__name__)

app = Dash(__name__, server=server, background_callback_manager=lc_manager)
app.title = "StorImages"
app.layout = storimages_layout


# show list of valid files
@app.callback([
    Output('preview_list', 'children'),
    Input('upload_area', 'contents'),
    Input('upload_area','filename'),
    ],
    prevent_initial_call=True
)
def show_uploaded_files(uploaded_contents, filename):
    # Must block if nothing is valid or loaded; unblock if things are valid
    # check if the upload is valid
    is_zip = filename.endswith('.zip')
    if not is_zip: # that is, if it could be a picture
        is_picture = file_is_supported(filename) # checks if picture is supported
        if is_picture:
            # show the preview to the user
            items_list = [show_items(filename)]
            return items_list
        else:
            # return an error about unsupported filename
            return [error_markdown]
        
    elif is_zip:
        decoded_contents = uploaded_content_handler(uploaded_contents, filename)[0] # contents
        files_in_zip = unzip(decoded_contents)
        files_processable = processable_items(files_in_zip)
        # show the files that can be processed to the user
        items_list = [show_items(files_processable)]
        return items_list

@app.callback(
    Output('preset_dimensions_div', 'children'),
    Input('preview_list', 'children'),
    suppress_callback_exceptions=True,
    prevent_initial_callback=True)
def show_preset_dimensions(preview_list):
    try:
        preview_content = preview_list['props']['children']
    except TypeError:
        preview_content = ''
    if preview_list: # if preview_list has children
        if 'refresh the webpage' not in preview_content:
            return preset_dimensions
    
@app.callback(
    Output('submit_button_div', 'children'),
    Input('thumbnail_sizes_dropdown', 'value'),
    suppress_callback_exceptions=True,
    prevent_initial_callback=True
    )
def show_upload_button(preset_dimensions_value):
    if preset_dimensions_value:
        return submit_button


@app.callback(
    [
        Output("download_image", "data"), # we will auto download
        State("upload_area", "contents"),
        State("upload_area", "filename"),
        State("thumbnail_sizes_dropdown", "value"),
        Input("submit_button", "n_clicks"),
    ],
    background=True,
    prevent_initial_call=True,
    suppress_callback_exceptions=True,
    manager=lc_manager
)
def submit_load(contents, filename, dimensions_selected, n_clicks):
    # only allow submission if everything is in place
    print(n_clicks)
    if n_clicks > 0:
        
        try:
            os.rmdir(shared_path)
            os.mkdir(shared_path)
        except Exception as e:
            pass
        
        is_zip = filename.endswith('.zip')
        is_picture = file_is_supported(filename) # checks if picture is supported
        decoded_contents = uploaded_content_handler(contents, filename)[0] # contents
        dimensions_array = resize_to_array(dimensions_selected)
        headers = {"Content-Type": "application/json"}
        zip_results_dir = os.path.join(shared_path, '')

        if is_picture:
            # save the file to disk
            path_to_pic = save_uploaded_picture(decoded_contents,filename)
            payload = generate_payload(filename, dimensions_array)
            print(payload)
            resizing_request = requests.post(endpoint, json=payload, headers=headers)
            print(resizing_request)
            response = resizing_request.json()
            print(response)
            picture_path = response['filename']
            resized_picture = load_picture_as_b(picture_path)
            print('sending picture')
            return resized_picture
            
        elif is_zip: # seq and not async because no time left
            extracted_to = extract_zip_to_disk(decoded_contents, filename) # extract to /storimages/data/{dirname}
            files_paths = [os.path.join(extracted_to, image) for image in os.listdir(extracted_to)]
            items_processable = processable_items(files_paths)
            payloads_to_be_sent = [generate_payload(file, dimensions_array) for file in items_processable]
            responses = [requests.post(endpoint, json=payload, headers=headers).json()['filename']
                          for payload in payloads_to_be_sent]
            zip_results_dir = '/storimages/data/resulting_zip'
            zipped_dir = f'{zip_results_dir}.zip'
            if os.path.exists(zip_results_dir):
                os.rmdir(zip_results_dir)
            if os.path.exists(zipped_dir):
                os.remove(zipped_dir)
            else:
                os.mkdir(zip_results_dir)
                zip_file_path = compress_into_zip(zipped_dir, responses)
                downloadable_zip = load_zip_as_b(zip_file_path)
                return downloadable_zip
if __name__ == "__main__":
    app.run(debug=False)
