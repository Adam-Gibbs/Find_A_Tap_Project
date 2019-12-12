import os
import json
from flask import Flask, redirect, request,render_template, jsonify, session, make_response, escape, flash
import sqlite3
import math
from datetime import date
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
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
# DeLancey, J. (2019). Getting Started with Geocoding Exif Image Metadata in Python 3 - HERE Developer. [online] HERE Developer Blog. Available at: https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3 [Accessed 8 Dec. 2019].
def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_geotagging(exif):
    geotagging = {}
    if exif == None:
        pass
    else:
        for (idx, tag) in TAGS.items():
            if tag == 'GPSInfo':
                if idx not in exif:
                    return None

                for (key, val) in GPSTAGS.items():
                    if key in exif[idx]:
                        geotagging[val] = exif[idx][key]

    return geotagging

def get_decimal_from_dms(dms, ref):
    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0
    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds
    return round(degrees + minutes + seconds, 5)
def get_coordinates(geotags):
    if geotags == None:
        lat = None
        lon = None
    elif len(geotags) == 0:
        lat = None
        lon = None
    else:
        lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
        lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
    return (lat,lon)
# finish reference

# lines 65 - 77 Janakiev, N. (2019). Calculate Distance Between GPS Points in Python. [online] Parametric Thoughts. Available at: https://janakiev.com/blog/gps-points-distance-python/ [Accessed 8 Dec. 2019].
def getDistance(latitude1, longitude1, latitude2, longitude2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = (latitude1, longitude1)
    lat2, lon2 = (latitude2, longitude2)

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2

    d = 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # finish reference
    if d <= 10: # This is 10 m (I think)
        return True
    else:
        return False

@app.route("/AddComment", methods = ['POST'])
def AddComment():
    if request.method =='POST':
        user_comment = request.json['commentData']
        tap_id = request.json['tapID']
        userId = session['userID']

        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("INSERT INTO reviews ('comment', 'date', 'tapID', 'userID')\
                            VALUES (?,date(julianday('now')),?,?)",(user_comment, tap_id, userId) )
            conn.commit()
        except:
            print('there was an error 0')
            conn.rollback()
        finally:
            conn.close()
    return "sucess"

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

@app.route("/home/taps/near/page=$<pagenum>$/!lat=<user_lat>&lng=<user_lng>", methods = ['GET'])
def NearTapPage(pagenum, user_lat, user_lng):
    if request.method =='GET':
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            # SQL command to order list by distance from longitude and latitude
            # Author:  statickidz
            # Date: 25/11/2019
            # Link: https://gist.github.com/statickidz/8a2f0ce3bca9badbf34970b958ef8479
            cur.execute("SELECT * FROM taps ORDER BY ((latitude-?)*(latitude-?)) + ((longitude - ?)*(longitude - ?)) ASC LIMIT ?, 5;", (user_lat, user_lat, user_lng, user_lng, int(pagenum)*5))
            data = cur.fetchall()
        except:
            print('there was an error 1')
            conn.close()
        finally:
            conn.close()

        all_tap_data = []
        for item in data:
            try:
                tapImage = Image.open(f"{APP_ROOT}{item[4]}",mode='r')
                tapImageRoute = item[4]
            except Exception as e:
                print(e)
                tapImageRoute = "http://placehold.it/750x300"
                print("failed to load")

            try:
                conn = sqlite3.connect(DATABASE)
                cur = conn.cursor()
                cur.execute("SELECT id, username FROM users WHERE id IS ?;", (str(item[5])))
                userdata = cur.fetchall()
                userdata = userdata[0]
            except:
                print('there was an error 2')
                conn.close()
            finally:
                conn.close()

            one_tap_data = {'TapID': item[0], 'Address': item[1], 'Longitude': item[3], 'Latitude': item[2], 'Image': tapImageRoute, 'Description': item[7], 'PostDate': item[6], 'UserLink': '/home/users/' + str(userdata[0]) + '/info', 'UserName': userdata[1]}
            all_tap_data.append(one_tap_data)

        return render_template('TapList.html', alltapdata = all_tap_data)

@app.route("/home/taps/search=£<search>£/page=$<pagenum>$/!lat=<user_lat>&lng=<user_lng>", methods = ['GET'])
def SearchTapPage(search, pagenum, user_lat, user_lng):
    if request.method =='GET':
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            # SQL command to order list by distance from longitude and latitude
            # Author:  statickidz
            # Date: 25/11/2019
            # Link: https://gist.github.com/statickidz/8a2f0ce3bca9badbf34970b958ef8479
            cur.execute("SELECT * FROM taps WHERE address LIKE ? ORDER BY ((latitude-?)*(latitude-?)) + ((longitude - ?)*(longitude - ?)) ASC LIMIT ?, 5;", ("%"+search+"%", user_lat, user_lat, user_lng, user_lng, int(pagenum)*5))
            data = cur.fetchall()
        except:
            print('there was an error 3')
            conn.close()
        finally:
            conn.close()

        all_tap_data = []
        for item in data:
            try:
                tapImage = Image.open(f"{APP_ROOT}{item[4]}",mode='r')
                tapImageRoute = item[4]
            except Exception as e:
                print(e)
                tapImageRoute = "http://placehold.it/750x300"
                print("failed to load")

            try:
                conn = sqlite3.connect(DATABASE)
                cur = conn.cursor()
                cur.execute("SELECT id, username FROM users WHERE id IS ?;", (str(item[5])))
                userdata = cur.fetchall()
                userdata = userdata[0]
            except:
                print('there was an error 4')
            finally:
                conn.close()

            one_tap_data = {'TapID': item[0], 'Address': item[1], 'Longitude': item[3], 'Latitude': item[2], 'Image': tapImageRoute, 'Description': item[7], 'PostDate': item[6], 'UserLink': '/home/users/' + str(userdata[0]) + '/info', 'UserName': userdata[1]}
            all_tap_data.append(one_tap_data)

        return render_template('TapList.html', alltapdata = all_tap_data)

@app.route("/home/taps/<tapID>/info", methods = ['GET'])
def TapInfo(tapID):
    if request.method =='GET':
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT * FROM taps WHERE id IS ?", [tapID])
            data = cur.fetchall()
            item = data[0]
        except:
            print('there was an error 5')
            conn.close()
        finally:
            conn.close()

        try:
            tapImage = Image.open(f"{APP_ROOT}{item[4]}",mode='r')
            tapImageRoute = item[4]
        except Exception as e:
            print(e)
            tapImageRoute = "http://placehold.it/900x300"
            print("failed to load")

        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT username FROM users WHERE id IS ?;", (str(item[5])))
            userdata = cur.fetchall()
            username = userdata[0][0]
        except:
            print('there was an error 6')
            conn.close()
        finally:
            conn.close()

        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT * from reviews WHERE tapID IS ?", ([str(item[0])]))
            commentdata = cur.fetchall()
        except:
            print('there was an error 7')
            commentdata = []
            conn.close()
        finally:
            conn.close()

        all_comment_data = []

        for comment in commentdata:

            try:
                conn = sqlite3.connect(DATABASE)
                cur = conn.cursor()
                cur.execute("SELECT id, userName from users WHERE id IS ?", (str(comment[4])))
                commentuserdata = cur.fetchall()
                commentuserdata = commentuserdata[0]
            except:
                print('there was an error 8')
                conn.close()
            finally:
                conn.close()

            one_comment_data= {'data': comment[1], 'date': comment[2], 'userLink': '/home/users/' + str(commentuserdata[0]) + '/info', 'username': commentuserdata[1]}
            all_comment_data.append(one_comment_data)


        one_tap_data = {'TapID': item[0], 'Address': item[1], 'Longitude': item[3], 'Latitude': item[2], 'Image': tapImageRoute, 'Description': item[7], 'PostDate': item[6], 'UserLink': '/home/users/' + str(item[5]) + '/info', 'UserName': username}

        return render_template('TapInfo.html', alltapdata = one_tap_data, allcommentdata = all_comment_data)

@app.route("/home/taps/<tapID>/location", methods = ['GET'])
def MapPage(tapID):
    if request.method =='GET':
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT latitude, longitude, address FROM taps WHERE id IS ?", [tapID])
            data = cur.fetchall()
            data = data[0]
        except:
            print('there was an error 9')
            conn.close()
        finally:
            conn.close()

        return render_template('PlainMap.html', lat = data[0], lng = data[1], address = data[2])

@app.route("/home/users/<userID>/info", methods = ['GET'])
def UserInfo(userID):
    if request.method =='GET':
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT username FROM users WHERE id IS ?;", [userID])
            data = cur.fetchall()
            data = data[0]
        except:
            print('there was an error')
            conn.close()
        finally:
            conn.close()

        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT id, address, picture, description FROM taps WHERE userID IS ? ORDER BY postDate DESC Limit 4;", [userID])
            tapdata = cur.fetchall()
        except:
            print('there was an error')
            conn.close()
        finally:
            conn.close()

        all_tap_data = []
        for item in tapdata:
            try:
                tapImage = Image.open(f"{APP_ROOT}{item[2]}",mode='r')
                tapImageRoute = item[2]
            except Exception as e:
                print(e)
                tapImageRoute = "https://placehold.it/700x400?text=Tap+Image+Here"
                print("failed to load")


            one_tap_data = {'TapID': item[0], 'Address': item[1], 'Picture': tapImageRoute, 'Description': item[3]}
            all_tap_data.append(one_tap_data)

        return render_template('UserInfo.html', userdata=data, alltapdata=all_tap_data)


@app.route("/home/taps/new/auto", methods = ['GET', 'POST'])
def NewTapPageAuto():
    msg = ''
    if request.method == 'GET':
        return render_template('addTapAuto.html')

    if request.method == 'POST':
        latitude = float(request.form["latitude"])
        longitude = float(request.form["longitude"])
        address = geocoder.reverse_geocode(latitude, longitude, language='en', no_annotations='1')
        address = address[0]['formatted']
        picture = request.files['picture']
        # if user does not select file, browser also submit a empty part without filename
        try:
            userId = session['userID']
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT latitude, longitude FROM taps WHERE latitude=? AND  longitude=?", (latitude, longitude))
            coor_exist = cur.fetchall()
            if len(coor_exist) == 0: # THIS IF STATEMENT MAKES SURE THAT TAPS THAT ALREADY EXIST IN THE DATABASE CANNOT BE INPUTTEED AGAIN
                if picture.filename == '': # This means that no picture was given
                        msg = "You have no picture, using manual to select location"
                        flash(msg)
                        return redirect('manual')
                else:
                    img_data = get_exif(picture)
                    geotags = get_coordinates(get_geotagging(img_data))
                    if geotags[0] and geotags[1] != None:
                        dist = getDistance(float(geotags[0]), float(geotags[1]), latitude, longitude)
                    else:
                        msg = "Picture doesn't have coordinates, please input the tap's location manualy"
                        flash(msg)
                        return redirect('manual')
                    if dist == True:
                        cur.execute("INSERT INTO taps (address, latitude, longitude, picture, userID, postDate) VALUES (?,?,?,?,?,date(julianday('now')))",
                        (address, latitude, longitude, f"/static/uploads/{picture.filename}", userId))
                        if picture and allowed_file(picture.filename): # we already know that a picture was given
                            filename = secure_filename(picture.filename)
                            filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                                os.makedirs(app.config['UPLOAD_FOLDER'])
                            picture.save(filePath)
                            msg = "Tap & Picture saved"
                        conn.commit()
                        flash(msg)
                        return redirect('/home')
                    elif dist == False:
                        msg = "You and the picture are not close enough"
                        flash(msg)
                        return redirect('manual')
            else:
                msg = "Tap already exists in the database"
                flash(msg)
                return redirect('auto')
        except Exception as e:
            msg = e
            conn.rollback()
            flash(msg)
            return redirect('manual')
        finally:
            conn.close()


@app.route("/home/taps/new/manual", methods = ['GET', 'POST'])
def NewTapPageManual():
    msg = ''
    if request.method == 'GET':
        return render_template('addTapManual.html')

    if request.method == 'POST':
        latitude = float(request.form["latitude"])
        longitude = float(request.form["longitude"])
        address = geocoder.reverse_geocode(latitude, longitude, language='en', no_annotations='1')
        address = address[0]['formatted']
        picture = request.files['picture']
        # if user does not select file, browser also submit a empty part without filename
        try:
            userId = session['userID']
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT latitude, longitude FROM taps WHERE latitude=? AND  longitude=?", (latitude, longitude))
            coor_exist = cur.fetchall()
            if len(coor_exist) == 0: # THIS IF STATEMENT MAKES SURE THAT TAPS THAT ALREADY EXIST IN THE DATABASE CANNOT BE INPUTTEED AGAIN
                if picture.filename == '': # This means that no picture was given
                    cur.execute("INSERT INTO taps (address, latitude, longitude, picture, userID, postDate) VALUES (?,?,?,?,?,date(julianday('now')))",
                    (address, latitude, longitude, None, userId))
                    conn.commit()
                    msg = "Tap saved"

                else:
                    cur.execute("INSERT INTO taps (address, latitude, longitude, picture, userID, postDate) VALUES (?,?,?,?,?,date(julianday('now')))",
                    (address, latitude, longitude, f"/static/uploads/{picture.filename}", userId))
                    if picture and allowed_file(picture.filename): # we already know that a picture was given
                        filename = secure_filename(picture.filename)
                        filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        if not os.path.exists(app.config['UPLOAD_FOLDER']):
                            os.makedirs(app.config['UPLOAD_FOLDER'])
                        picture.save(filePath)
                        msg = "Tap & Picture saved"
                    conn.commit()

                flash(msg)
                return redirect('/home')

            else:
                flash("Tap already exists in the database")
                return redirect('manual')
        except Exception as e:
            msg = e
            conn.rollback()
            flash("There was an error inserting the tap")
            return redirect('manual')
        finally:
            conn.close()

@app.route("/givetaps", methods = ['POST'])
def GiveTaps():
    if request.method =='POST':
        user_lat = request.json['lat']
        user_lng = request.json['lng']
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            # SQL command to order list by distance from longitude and latitude
            # Author:  statickidz
            # Date: 25/11/2019
            # Link: https://gist.github.com/statickidz/8a2f0ce3bca9badbf34970b958ef8479
            cur.execute("SELECT id, address, latitude, longitude, picture FROM taps ORDER BY ((latitude-?)*(latitude-?)) + ((longitude - ?)*(longitude - ?)) ASC;", (user_lat, user_lat, user_lng, user_lng))
            data = cur.fetchall()
        except:
            print('there was an error 11')
            conn.close()
        finally:
            conn.close()

        all_tap_data = []
        for item in data:
            try:
                tapImage = Image.open(f"{APP_ROOT}{item[4]}",mode='r')
                tapImage = item[4]
            except Exception as e:
                print(e)
                tapImage = "https://placehold.it/500?text=Tap+Image+Here"
                print("failed to load")

            one_tap_data = {'ID': item[0], 'Address': item[1], 'Lat': item[2], 'Lng': item[3], 'Image': tapImage}
            all_tap_data.append(one_tap_data)

        return jsonify(all_tap_data)

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

@app.route("/home/login/admin", methods = ['GET', 'POST'])
#code for deleting a row in a database: DELETE FROM "main"."users" WHERE _rowid_ IN ('1');
def AdminPage():
    # if session.get('admin') is not True:
    #     return redirect("/", code=302)
    username = request.cookies.get('username')
    usertype = "null"
    if 'usertype' in session:
        usertype = escape(session['usertype'])
    if usertype == "Admin":
        if request.method =='GET':
            return render_template('adminPage.html', msg = '', username = username)
    else:
        return render_template('HomePage.html', username = username)

@app.route("/home/signup", methods = ['GET','POST'])
def SignupPage():
    if request.method =='GET':
        return render_template('Signup.html')
    if request.method =='POST':
        usern = request.form.get('UN', default="Error")
        passw = request.form.get('PW', default="Error")
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("INSERT INTO users ('userName', 'password', 'role')\
                        VALUES (?,?,?)",(usern, passw, '0') )
            conn.commit()
        except:
            conn.rollback()
            return redirect("/", code=302)
        finally:
            conn.close()
            return render_template('Signup.html')

@app.route("/home/login", methods = ['GET','POST'])
def LoginPage():
    if request.method =='GET':
        return render_template('login_page.html')
    if request.method=='POST':
        uName = request.form.get('username', default="Error")
        pw = request.form.get('password', default="Error")
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT id, role FROM users WHERE userName IS ? AND password IS ?", (uName, pw))
        data = cur.fetchall()
        data = data[0]
        # conn.commit()
        if data[1] == 1:
            session['usertype'] = 'Admin'
            session['userID'] = data[0]
            return redirect("/home/login/admin", code=302)
        else:
            session['usertype'] = 'Customer'
            session['userID'] = data[0]
            return redirect("/home", code=302)

    else:
        return render_template('login_page.html')

@app.route("/home/login/admin/tapsDB", methods = ['GET', 'POST'])
def tapsDBPage():
	if request.method =='GET':
            try:
                conn = sqlite3.connect(DATABASE)
                cur = conn.cursor()
                cur.execute("SELECT * FROM taps")
                data = cur.fetchall()
            except:
                print('there was an error 12')
                conn.close()
                return redirect("/home/login/admin", code=302)
            finally:
                conn.close()
                return render_template('tapsAP.html', data = data)

@app.route("/home/login/admin/reviewsDB", methods = ['GET', 'POST'])
def reviewsDBPage():
	if request.method =='GET':
            try:
                conn = sqlite3.connect(DATABASE)
                cur = conn.cursor()
                cur.execute("SELECT * FROM reviews")
                data = cur.fetchall()
            except:
                print('there was an error 13')
                conn.close()
                return redirect("/home/login/admin", code=302)
            finally:
                conn.close()
                return render_template('reviewAP.html', data = data)

@app.route("/home/login/admin/usersDB", methods = ['GET', 'POST'])
def usersDBPage():
	if request.method =='GET':
            try:
                conn = sqlite3.connect(DATABASE)
                cur = conn.cursor()
                cur.execute("SELECT * FROM users")
                data = cur.fetchall()
            except:
                print('there was an error 14')
                conn.close()
                return redirect("/home/login/admin", code=302)
            finally:
                conn.close()
                return render_template('usersAP.html', data = data)

@app.route("/deleteTap", methods = ['DELETE'])
def deleteTapPage():
	if request.method =='DELETE':
            tapDelete = request.form.get('idDelete', default="Error")
            try:
                conn = sqlite3.connect(DATABASE)
                cur = conn.cursor()
                cur.execute("DELETE FROM taps WHERE id IS ?;", (tapDelete))
                conn.commit()
            except:
                print('there was an error 15')
                conn.rollback()
            finally:
                conn.close()
                return "Success"

@app.route("/deleteUser", methods = ['DELETE'])
def deleteUserPage():
	if request.method =='DELETE':
            userDelete = request.form.get('idDelete', default="Error")
            try:
                conn = sqlite3.connect(DATABASE)
                cur = conn.cursor()
                cur.execute("DELETE FROM users WHERE id IS ?;", (userDelete))
                conn.commit()
            except:
                print('there was an error 16')
                conn.rollback()
            finally:
                conn.close()
                return "Success"

@app.route("/deleteReview", methods = ['DELETE'])
def deleteReviewPage():
	if request.method =='DELETE':
            reviewDelete = request.form.get('idDelete', default="Error")
            try:
                conn = sqlite3.connect(DATABASE)
                cur = conn.cursor()
                cur.execute("DELETE FROM reviews WHERE id IS ?;", (reviewDelete))
                conn.commit()
            except:
                print('there was an error 17')
                conn.rollback()
            finally:
                conn.close()
                return "Success"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, ssl_context='adhoc')
