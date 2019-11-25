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



# @app.route("/Directory", methods=['GET'])
# def returnDir():
#     if request.method == 'GET':
#         print("getting directory.")
#         return json.dumps(directory)

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

# @app.route("/AddComment", methods = ['POST','GET'])
# def studentAddDetails():
#     if request.method =='GET':
#         return flask.redirect('CommentsTaps.html')
#     if request.method =='POST':
#         add_comment_to_db = request.form.get('comments', default="Error")
#         add_date_to_db = request.form.get('date', default="Error")
#         print("inserting comment "+add_comment_to_db)
#         try:
#             conn = sqlite3.connect(DATABASE)
#             cur = conn.cursor()
#             sqlquery = 'INSERT INTO "main"."reviews" ("tap-id", "comment", "date") VALUES ("1", "' + add_comment_to_db + '", "'+ add_date_to_db +'");'
#             print(sqlquery)
#             cur.execute(sqlquery)
#             conn.commit()
#             msg = add_comment_to_db
#         except:
#             conn.rollback()
#             msg = "error in insert operation"
#         finally:
#             conn.close()
#             return msg

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
        print(coordinates)
        latitude = coordinates.split(",")[0]
        longitude = coordinates.split(",")[1]
        address = geocoder.reverse_geocode(latitude, longitude, language='en', no_annotations='1')
        print(address[0]['formatted'])
        # picture = params['picture']
        # print(picture)
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
