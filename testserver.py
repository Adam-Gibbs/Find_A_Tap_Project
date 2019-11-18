from flask import Flask, redirect, request, render_template

app = Flask(__name__)

@app.route("/Where", methods = ['GET'])
def WherePage():
	if request.method =='GET':
		return redirect('/static/index.html')

if __name__ == "__main__":
	app.run(host='10.204.195.91', port=5000)
