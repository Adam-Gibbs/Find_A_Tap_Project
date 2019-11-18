import os
import json
from flask import Flask, redirect, request,render_template, jsonify

app = Flask(__name__)

@app.route("/AddContact", methods=['POST'])
def addContact():
    print('processing Data')
    message ='already there'
    if request.method == 'POST':
        name = request.form['name']
        num = request.form['num']
        if not(name in directory):
            message = 'ok'
            directory[name] =  num
        print(directory)
    return message

if __name__ == "__main__":
    app.run(debug=True)