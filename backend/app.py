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
    thumbnail_request = request.json
    filename = thumbnail_request['filename']
    new_dimensions = thumbnail_request['dimensions']
    # returns the string of the new filename; filename_dimensionXdimension.ext;; just the path
    resized_image = resize_image(filename, new_dimensions)
    # add a try-except
    # response = {thumbnail_request + filename:path} | {thumbnail_request + filename:''};; we need to log errors at least
    thumbnail_response = {

    }
    jsonify(thumbnail_response)
    pass

if __name__ == "__main__":
    app.run(debug=True)
