from flask import Flask, request, redirect
import binascii
import base64
import ipythonify 
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/redirect', methods=['GET', 'POST'])
def make_redirect_ipython():
    archive = request.args.get('archive')
    ipythonify.pyprep(archive, '/home/user/asdf', 'asdf')
    notebook = ipythonify.jsonify('/home/user/asdf/asdf.py', '/home/user/asdf/asdf.ipynb') 
    with open("/home/user/asdf/asdf.ipynb", "w") as notebook_file:
        notebook_file.write(notebook)

    return redirect('http://localhost:8888', code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
