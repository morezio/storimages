from flask import Flask, request, jsonify
from be_fns import resize_image
# this is to be served with gunicorn at runtime
app = Flask(__name__)

# receives a path and dimensions to transform
# returns a path if success
# empty or crashes if not
@app.route("/create_thumbnail", methods=["POST"])
def create_thumbnail():
    # receive the name of the picture and dimensions from the body
    thumbnail_request = request.get_json()
    filename = thumbnail_request['filename']
    new_dimensions = thumbnail_request['dimensions']
    # for when receiving a JSON array through curl
    if isinstance(new_dimensions,list):
        new_dimensions = tuple(new_dimensions)
    print(new_dimensions)
    # returns the string of the new filename; filename_dimensionXdimension.ext;; just the path
    resized_image = resize_image(filename, new_dimensions)
    # add a try-except
    # response = {thumbnail_request + filename:path} | {thumbnail_request + filename:''};; we need to log errors at least
    thumbnail_response = {}
    thumbnail_response['request'] = thumbnail_request
    thumbnail_response['filename'] = resized_image
    return jsonify(thumbnail_response)
if __name__ == "__main__":
    app.run(debug=True, port=80)
