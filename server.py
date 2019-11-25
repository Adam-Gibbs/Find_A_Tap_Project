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

@app.route("/home/taps/near/page={pagenum}", methods = ['GET'])
def NearTapPage(pagenum):
    if request.method =='GET':
        return render_template('TapList.html')
    if request.method =='POST':
		try:
			conn = sqlite3.connect(DATABASE)
			cur = conn.cursor()
			cur.execute(f"SELECT \
                            id, ( \
                            6371 * acos ( \
                            cos ( radians({user_lat}) ) \
                            * cos( radians( lat ) ) \
                            * cos( radians( lng ) - radians({user_lng}) ) \
                            + sin ( radians({user_lat}) ) \
                            * sin( radians( lat ) ) \
                            ) \
                        ) AS distance \
                        FROM table \
                        HAVING distance < 30 \
                        ORDER BY distance \
                        LIMIT {pagenum*5} , 5; ") 
			data = cur.fetchall()
			print(data)
		except:
			print('there was an error')
			conn.close()
		finally:
			conn.close()

@app.route("/home/taps/new", methods = ['GET', 'POST'])
def NewTapPage():
    if request.method == 'GET':
        return render_template('addTap.html')
    if request.method == 'POST':
        params = request.form
        params = params.to_dict() # This is from flask
        print("------------------------------------------------------------------------",params)
        latitude = params['latitude']
        longitude = params['longitude']
        address = geocoder.reverse_geocode(latitude, longitude, language='en', no_annotations='1')
        address = address[0]['formatted']
        print(address)
        picture = params['picture']
        print(picture)
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("INSERT INTO taps (address, latitude, longitude, picture) VALUES (?,?,?,?)",
            (address, latitude, longitude, picture))
            conn.commit()
            msg = "Task was executed: True"
        except Exception as e:
            print(e)
            conn.rollback()
            msg = f"Task failed because: {e}"
            if e == "UNIQUE constraint failed: taps.coordinates":
                msg = ''' var error = document.getElementById('error-message');
                    error.innerHTML = Tap already exists;
                '''
        finally:
            conn.close()
            return msg

@app.route("/home/taps/page={pagenum}", methods = ['GET', 'POST'])
def AllTapsPage(pagenum):
    if request.method =='GET':
        return render_template('TapList.html')
	if request.method =='POST':
		try:
			conn = sqlite3.connect(DATABASE)
			cur = conn.cursor()
			cur.execute(f"SELECT * FROM taps LIMIT {pagenum*5} , 5; ") 
			data = cur.fetchall()
			print(data)
		except:
			print('there was an error')
			conn.close()
		finally:
			conn.close()

@app.route("/home/faq", methods = ['GET'])
def FAQPage():
    if request.method =='GET':
        return render_template('FAQ.html')

@app.route("/home/about/contact", methods = ['GET'])
def ContactPage():
    if request.method =='GET':
        return render_template('Contact.html')

@app.route("/home/taps/comments", methods = ['GET'])
def CommentsPage():
	if request.method =='GET':
		return render_template('CommentsTaps.html')

@app.route("/home/taps/tapID/location", methods = ['GET'])
def MapPage():
	if request.method =='GET':
		return render_template('PlainMap.html')

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')
