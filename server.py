import os
import json
from flask import Flask, redirect, request,render_template, jsonify
import sqlite3
# Below 4 lines are for Geocode coordinate and error handling for all geocoder files
# FOR THIS TO WORK YOU NEED TO ON YOUR CMD TO DO THIS: pip install opencage
from opencage.geocoder import OpenCageGeocode
from opencage.geocoder import InvalidInputError, RateLimitExceededError, UnknownError
key = 'd0d06fa6997b4770af8c48796657cbf0'
geocoder = OpenCageGeocode(key)

DATABASE = 'databases/main_db.db'
app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
directory = []

@app.route("/saveCoordinates", methods=['POST','GET'])
def addLocation():
    if request.method =='GET':
        return redirect('/static/index.html')
    elif request.method =='POST':
        print(type(request.form))
        params = request.form
        params = params.to_dict() # This is from flask
        print("------------------------------------------------------------------------",params)
        coordinates = params['coordinates']
        address = params['address']
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("INSERT INTO taps (address, coordinates) VALUES (?,?)",
            (address, coordinates))
            conn.commit()
            executed = True
        except:
            conn.rollback()
            print("An error has occured when accessing the database")
            executed = False
        finally:
            conn.close()
            return f"Task was executed: {executed}"

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
            directory.append(comments)
        print(directory)
    return message

@app.route("/", methods = ['GET'])
def HomeRedirect():
    if request.method =='GET':
        return redirect('/home')

@app.route("/home", methods = ['GET'])
def HomePage():
    if request.method =='GET':
        return render_template('HomePage.html')

@app.route("/home/about", methods = ['GET'])
def AboutPage():
    if request.method =='GET':
        return render_template('About.html')

@app.route("/home/taps/near", methods = ['GET'])
def NearTapPage():
    if request.method =='GET':
        return render_template('TapList.html')

@app.route("/home/taps/new", methods = ['GET', 'POST'])
def NewTapPage():
    if request.method == 'GET':
        return render_template('addTap.html')
    if request.method == 'POST':
        params = request.form
        params = params.to_dict() # This is from flask
        print("------------------------------------------------------------------------",params)
        coordinates = params['coordinates']
        latitude = coordinates.split(",")[0]
        longitude = coordinates.split(",")[1]
        address = geocoder.reverse_geocode(latitude, longitude, language='en', no_annotations='1')
        print(address[0]['formatted'])
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("INSERT INTO taps (address, coordinates) VALUES (?,?)",
            (address[0]['formatted'], coordinates))
            conn.commit()
            executed = True
        except Exception as e:
            print(e)
            conn.rollback()
            executed = False
        finally:
            conn.close()
            return f"Task was executed: {executed}"

@app.route("/home/taps", methods = ['GET'])
def AllTapsPage():
    if request.method =='GET':
        return render_template('TapList.html')

@app.route("/home/faq", methods = ['GET'])
def FAQPage():
    if request.method =='GET':
        return render_template('FAQ.html')

@app.route("/home/about/contact", methods = ['GET'])
def ContactPage():
    if request.method =='GET':
        return render_template('Contact.html')

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')
