#!flask/bin/python
from flask import Flask, request
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/<path:filename>')
def static_proxy(filename):
	return send_from_directory('static', filename)

if __name__ == '__main__':
	app.run(debug=True)