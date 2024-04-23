# flask_app.py
from flask import Flask, request, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins


# Endpoint for proxying requests
@app.route("/proxy")
def proxy():
    url = request.args.get("url")
    response = requests.get(url)
    return Response(response.content, content_type=response.headers['Content-Type'])