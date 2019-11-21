from flask import Flask, redirect, request, render_template

app = Flask(__name__)

@app.route("/where", methods = ['GET'])
def WherePage():
	if request.method =='GET':
		return redirect('/static/index.html')

@app.route("/home", methods = ['GET'])
def HomePage():
	if request.method =='GET':
		return render_template('HomePage.html')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
