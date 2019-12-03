import os
import json
from flask import Flask, redirect, request,render_template, jsonify, session, make_response, escape
import sqlite3

# Below 4 lines are for Geocode coordinate and error handling for all geocoder files
# FOR THIS TO WORK YOU NEED TO ON YOUR CMD TO DO THIS: pip install opencage
from opencage.geocoder import OpenCageGeocode
from opencage.geocoder import InvalidInputError, RateLimitExceededError, UnknownError
from werkzeug.utils import secure_filename
key = 'd0d06fa6997b4770af8c48796657cbf0'
geocoder = OpenCageGeocode(key)

APP_ROOT = os.path.dirname(os.path.abspath(__file__)) # This says where the server is stored on the device
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads') # This adds the folder where the tap pictures are going to be stored
DATABASE = 'databases/main_db.db'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
directory = []
app.secret_key = 'fj590Rt?h40gg'

def allowed_file(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and ext in ALLOWED_EXTENSIONS

def checkCredentials(uName, pw):
    return pw == 'funky'

@app.route("/AddComment", methods = ['POST','GET'])
def studentAddDetails():
    if request.method =='GET':
        return flask.redirect('CommentsTaps.html')
    if request.method =='POST':
        add_comment_to_db = request.form.get('comments', default="Error")
        add_date_to_db = request.form.get('date', default="Error")
        print("inserting comment "+add_comment_to_db)
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            sqlquery = 'INSERT INTO "main"."reviews" ("comment", "date") VALUES ("' + add_comment_to_db + '", "'+ add_date_to_db +'");'
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

@app.route("/home/about/why" , methods = ['GET'])
def WhyUseTapspage():
    if request.method =='GET':
        return render_template('FAQ.html')

@app.route("/home/taps/near/page=<pagenum>/!lat=<user_lat>&lng=<user_lng>", methods = ['GET'])
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
            try:
                print(item[4])
                tapImage = Image.open(f"{APP_ROOT}{item[4]}")
                print(tapImage.filename)
            except Exception as e:
                print(e)
                tapImage = "http://placehold.it/750x300"
                print("failed to load")
            print(f"-----------------------------------------{tapImage}")
            print(f"--------------------------------------------------{APP_ROOT}{item[4]}")
            one_tap_data = {'TapID': item[0], 'Address': item[1], 'Longitude': item[2], 'Latitude': item[3], 'Image': tapImage, 'Description': 'Temporary Description', 'PostDate': "26/11/2019", 'UserLink': 'https://www.linkedin.com/in/adam-gibbs-77411616b/', 'UserName': 'Adam'}
            all_tap_data.append(one_tap_data)

        return render_template('TapList.html', alltapdata = all_tap_data)

@app.route("/home/taps/new/auto", methods = ['GET', 'POST'])
def NewTapPageAuto():
    msg = ''
    global post_info
    if request.method == 'GET':
        return render_template('addTapAuto.html')

    if request.method == 'POST':
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        address = geocoder.reverse_geocode(latitude, longitude, language='en', no_annotations='1')
        address = address[0]['formatted']
        picture = request.files['picture']
        # if user does not select file, browser also submit a empty part without filename
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT latitude, longitude FROM taps WHERE latitude=? AND  longitude=?", (latitude, longitude))
            coor_exist = cur.fetchall()
            ## THIS IF STATEMENT MAKES SURE THAT TAPS THAT ALREADY EXIST IN THE DATABASE CANNOT BE INPUTTEED AGAIN
            if len(coor_exist) == 0:
                if picture.filename == '': # This means that no picture was given
                    cur.execute("INSERT INTO taps (address, latitude, longitude, picture, userID) VALUES (?,?,?,?,?)",
                    (address, latitude, longitude, None, 1))
                else:
                    cur.execute("INSERT INTO taps (address, latitude, longitude, picture, userID) VALUES (?,?,?,?,?)",
                    (address, latitude, longitude, f"static/uploads/{picture.filename}", 1))
                    if picture.filename == '':
                        msg = 'picture was not given'
                    elif picture and allowed_file(picture.filename):
                        filename = secure_filename(picture.filename)
                        filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'])):
                            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER']))
                        picture.save(filePath)
                        msg += "picture was saved"
                conn.commit()
                msg = "Task was executed"
            else:
                msg = "Tap already exists in the database"
            location = '/home/taps/new/auto'
            print(msg, location)
            return redirect('auto')
        except Exception as e:
            print(e)
            conn.rollback()
            print("rolled back")
            return redirect('manual')
        finally:
            conn.close()

@app.route("/home/taps/new/manual", methods = ['GET'])
def NewTapPageManual():
    msg = ''
    if request.method == 'GET':
        print("hello2")
        return render_template('addTapManual.html')


@app.route("/home/taps/page=<pagenum>", methods = ['GET'])
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

@app.route("/home/taps/<tapID>/location", methods = ['GET'])
def MapPage(tapID):
    if request.method =='GET':
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            # https://gist.github.com/statickidz/8a2f0ce3bca9badbf34970b958ef8479
            cur.execute("SELECT latitude, longitude, address FROM taps WHERE id IS ?", [tapID])
            data = cur.fetchall()
            data = data[0]
            print(data[0])
            print(data[1])
            print(data[2])
        except:
            print('there was an error')
            conn.close()
        finally:
            conn.close()

        return render_template('PlainMap.html', lat = data[0], lng = data[1], address = data[2])

@app.route("/home/login/admin", methods = ['GET', 'POST'])
#code for deleting a row in a database: DELETE FROM "main"."users" WHERE _rowid_ IN ('1');
def AdminPage():
    username = request.cookies.get('username')
    usertype = "null"
    if 'usertype' in session:
        usertype = escape(session['usertype'])
    print(usertype)
    if usertype == "Admin":
        print(usertype)
        if request.method =='GET':
            try:
                conn = sqlite3.connect(DATABASE)
                print(DATABASE)
                cur = conn.cursor()
                cur.execute("SELECT * FROM users")
                # cur.execute("SELECT * FROM Modules WHERE name=? AND  credits='20' ;", [name])
                data = cur.fetchall()
                print(data)
            except:
                print('there was an error', data)
                conn.close()
            finally:
                conn.close()
                #return str(data)
                return render_template('adminPage.html', data = data, username = username)
        # return render_template('adminPage.html', msg = '', username = username)
    else:
        return render_template('HomePage.html', msg = 'no access to admin pages', username = username)
    # if request.method =='GET':
    #     try:
    #         conn = sqlite3.connect(DATABASE)
    #         cur = conn.cursor()
    #         cur.execute("SELECT * FROM users")
    #         # cur.execute("SELECT * FROM Modules WHERE name=? AND  credits='20' ;", [name])
    #         data = cur.fetchall()
    #         print(data)
    #     except:
    #         print('there was an error', data)
    #         conn.close()
    #     finally:
    #         conn.close()
    #         #return str(data)
    #         return render_template('adminPage.html', data = data)

@app.route("/home/login", methods = ['GET','POST'])
def LoginPage():
    if request.method =='GET':
        return render_template('login_page.html')
    if request.method=='POST':
        reminder =". ***** REM other pages WILL NOT be able to access the username as they are not set up to use Cookie Sessions. "
        uName = request.form.get('username', default="Error")
        pw = request.form.get('password', default="Error")
        if checkCredentials(uName, pw):
            resp = make_response(render_template('adminPage.html', msg='hello '+uName+reminder, username = uName))
            session['username'] = request.form['username']
            print('username')
            session['password'] = 'pa55wrd'
            if (uName == 'Osama'):
                 session['usertype'] = 'Admin'
                 return redirect("/home/login/admin", code=302)
            else:
                 session['usertype'] = 'Customer'
                 return redirect("/home", code=302)

        else:
            resp = make_response(render_template('login_page.html', msg='Incorrect  login',username='Guest'))
        return resp
    else:
        username = 'none'
        if 'username' in session:
            username = escape(session['username'])
        return render_template('login_page.html', msg='', username = username)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')
