import diskcache, flask
from dash import DiskcacheManager, Dash
from dash.dependencies import Input, Output, State

from components import storimages_layout

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
@app.callback()
def show_uploaded_files():
    # if .zip: unzip and check all files are valid
    # if single image: check is valid
    # if valid, confirm submit; if not valid, refresh and start over
    pass

@app.callback(
    [
        Output("download_legend_div", "children"),
        Input("submit_button", "n_clicks"),
        State("thumbnail_sizes_dropdown_multiselect", "value"),
        State("other_thumbnail_singleselect", "value"),
    ],
    background=True,
    prevent_initial_call=True,
    manager=lc_manager,
)
def submit_load(n_clicks, thumbnail_sizes, other_thumbnail_single):
    pass


if __name__ == "__main__":
    app.run(debug=True)
