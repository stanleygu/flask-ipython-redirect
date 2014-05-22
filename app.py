from flask import Flask, request, redirect
import binascii
import base64
import ipythonify 
import os, sys

app = Flask(__name__)

home = os.path.dirname(sys.executable)
usrdir = os.path.expanduser('~')
dirname = os.path.join(usrdir, 'intPDF')

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/redirect', methods=['GET', 'POST'])
def make_redirect_ipython():
    archive = request.args.get('archive')
    ipythonify.pyprep(archive, dirname, 'a')
    notebook = ipythonify.jsonify(os.path.join(dirname,'a.py'), 'a.ipynb')
    with open(os.path.join(dirname,'a.ipynb'), "w") as notebook_file:
        notebook_file.write(notebook)

    return redirect('http://localhost:8888/notebooks/' + 'a.ipynb', code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
