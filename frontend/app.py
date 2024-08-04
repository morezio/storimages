import diskcache, flask
from dash import DiskcacheManager, Dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from components import (storimages_layout, submit_button, preset_dimensions,
                        error_markdown)
from fe_fns import (uploaded_content_handler, file_is_supported, 
                    processable_items, unzip, show_items, extract_zip_to_disk,
                    save_uploaded_picture, resize_to_array)

# app.py = essentially the app you interact with
# I move layout to another file to make it easier to follow


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
        # Output("download_button_div", "children"), # we will auto download
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
    if n_clicks > 0:
        
        is_zip = filename.endswith('.zip')
        is_picture = file_is_supported(filename) # checks if picture is supported
        decoded_contents = uploaded_content_handler(contents, filename)[0] # contents
        dimensions = resize_to_array(dimensions_selected)
        
        if is_picture:
            # save the file to disk
            path_to_pic = save_uploaded_picture(decoded_contents)
            
            # send a single request
            # download automatically the file
            pass
            
        elif is_zip:
            extract_zip_to_disk(decoded_contents) # extract to /storimages/{filename}

            pass


if __name__ == "__main__":
    app.run(debug=True)
