import os
import json
from flask import Flask, redirect, request,render_template, jsonify
import sqlite3

DATABASE = 'databases/main_db.db'
app = Flask(__name__)

@app.route("/saveCoordinates", methods=['POST','GET'])
def addLocation():
    if request.method =='GET':
        return redirect('/static/index.html')
    elif request.method =='POST':
        print(type(request.form))
        params = request.form
        params = params.to_dict() # This is from flask
        print("------------------------------------------------------------------------",params)
        longitude = params['longitude']
        latitude = params['latitude']
        address = params['address']
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("INSERT INTO taps (address, longitude, latitude) VALUES (?,?,?)",
            (address, longitude, latitude))
            conn.commit()
            executed = True
        except:
            conn.rollback()
            print("An error has occured when accessing the database")
            executed = False
        finally:
            conn.close()
            return f"Task was executed: {executed}"

if __name__ == "__main__":
    app.run(debug=True)
