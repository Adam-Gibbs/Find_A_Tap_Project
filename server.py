import os
import json
from flask import Flask, redirect, request,render_template, jsonify
import sqlite3
# Below 4 lines are for Geocode coordinate and error handling for all geocoder files
# FOR THIS TO WORK YOU NEED TO ON YOUR CMD TO DO THIS: pip install opencage
from opencage.geocoder import OpenCageGeocode
from opencage.geocoder import InvalidInputError, RateLimitExceededError, UnknownError
from werkzeug.utils import secure_filename
key = 'd0d06fa6997b4770af8c48796657cbf0'
geocoder = OpenCageGeocode(key)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))# this
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
DATABASE = 'databases/main_db.db'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
directory = []

@app.route("/AddComment", methods = ['POST','GET'])
def studentAddDetails():
    if request.method =='GET':
        return flask.redirect('CommentsTaps.html')
    if request.method =='POST':
        add_comment_to_db = request.form.get('comments', default="Error")
        add_date_to_db = request.form.get('date', default="Error")
        print("inserting comment "+add_comment_to_db)
        try:
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            sqlquery = 'INSERT INTO "main"."reviews" ("tap-id", "comment", "date") VALUES ("1", "' + add_comment_to_db + '", "'+ add_date_to_db +'");'
            print(sqlquery)
            cur.execute(sqlquery)
            conn.commit()
            msg = add_comment_to_db
        except:
            conn.rollback()
            msg = "error in insert operation"
        finally:
            conn.close()
            return msg

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

@app.route("/home/taps/near/page=<pagenum>/lat=<user_lat>/lng=<user_lng>", methods = ['GET'])
def NearTapPage(pagenum, user_lat, user_lng):
    if request.method =='GET':
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            # https://gist.github.com/statickidz/8a2f0ce3bca9badbf34970b958ef8479
            cur.execute("SELECT * FROM taps ORDER BY ((latitude-?)*(latitude-?)) + ((longitude - ?)*(longitude - ?)) ASC LIMIT ?, 5;", (user_lat, user_lat, user_lng, user_lng, int(pagenum)*5))
            data = cur.fetchall()
        except:
            print('there was an error')
            conn.close()
        finally:
            conn.close()
        
        all_tap_data = []
        for item in data:
            one_tap_data = {'TapID': item[0], 'Address': item[1], 'Longitude': item[2], 'Latitude': item[3], 'Image': item[4], 'Description': 'Temporary Description', 'PostDate': "26/11/2019", 'UserLink': 'https://www.linkedin.com/in/adam-gibbs-77411616b/', 'UserName': 'Adam'}
            all_tap_data.append(one_tap_data)

        return render_template('TapList.html', alltapdata = all_tap_data)

    if request.method =='POST':
        pass

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
        picture = params['picture']
        # picture = request.files['picture']
        print(picture)
        if len(picture) > 0:
            picture_extension = picture.split(".")[1].lower()
            print(picture_extension)
            if picture_extension not in ALLOWED_EXTENSIONS:
                picture = None
                # this makes sure that only picture type files are uploaded to the website
        if picture != None and len(picture) != 0: # This means that the picture exists
            picture = picture.split("\\")[2]
            print("------------------------------------------------------------------------------------------------------------------------------",picture)
            # filename = secure_filename(picture.filename)
            # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # picture.save(filepath)
            # print("Done")
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT latitude, longitude FROM taps WHERE latitude=? AND  longitude=?", (latitude, longitude))
            data = cur.fetchall()
            ## THIS IF STATEMENT MAKES SURE THAT TAPS THAT ALREADY EXIST IN THE DATABASE CANNOT BE INPUTTEED AGAIN
            if len(data) == 0:
                cur.execute("INSERT INTO taps (address, latitude, longitude, picture) VALUES (?,?,?,?)",
                (address, latitude, longitude, picture))
                conn.commit()
                msg = "Task was executed"
            else:
                msg = "Tap already exists in the database"
                #alert(msg)
        except Exception as e:
            print(e)
            conn.rollback()
            msg = f"Task failed because: {e}"
        finally:
            conn.close()
            return msg

@app.route("/home/taps/page=<pagenum>", methods = ['GET', 'POST'])
def AllTapsPage(pagenum):
    if request.method =='GET':
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM taps LIMIT ?, 5; ", (int(pagenum)*5))
            data = cur.fetchall()
            print(data)
        except:
            print('there was an error')
            conn.close()
        finally:
            conn.close()
        return render_template('TapList.html')
    if request.method =='POST':
        pass

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
