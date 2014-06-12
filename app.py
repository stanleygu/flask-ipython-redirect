from flask import Flask, request, redirect, render_template
import ipythonify
import os
import sys

app = Flask(__name__)

home = os.path.dirname(sys.executable)
usrdir = os.path.expanduser('~')
dirname = os.path.join(usrdir, 'intPDF')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/redirect', methods=['GET', 'POST'])
def make_redirect_ipython():
    return render_template('pickHost.html')


@app.route('/open')
def openAsNotebook():
    # host = request.args.get('host')

    title = request.args.get('title', type=str)
    encin = request.args.get('format', type=str)
    archive = request.args.get('archive', type=str)
    host = request.args.get('host', type=str)
    ipythonify.pyprep(archive, dirname, title, encin)
    notebook = ipythonify.jsonify(os.path.join(dirname, title + '.py'), title)
    with open(os.path.join(dirname, title + '.ipynb'), "w") as notebook_file:
        notebook_file.write(notebook)

    return redirect('http://' + host + '/notebooks/' +
                    title + '.ipynb', code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
