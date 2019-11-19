import os
import json
from flask import Flask, redirect, request,render_template, jsonify

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
directory = {}

app = Flask(__name__)

@app.route("/Directory", methods=['GET'])
def returnDir():
    if request.method == 'GET':
        print("getting directory.")
        return json.dumps(directory)

@app.route("/AddComment", methods=['POST'])
def addComment():
    print('processing Data')
    message ='already there'
    if request.method == 'POST':
        comments = request.form['comments']
        if not(comments in directory):
            message = comments
            directory[comments] =  comments
        print(directory)
    return message

if __name__ == "__main__":
    app.run(debug=True)