from flask import Flask, request, jsonify

# this is to be served with gunicorn at runtime
server = Flask(__name__)