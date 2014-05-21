from flask import Flask, request, redirect
import binascii
import base64
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


def decodeString(s):
    try:
        return binascii.unhexlify(s)
    except TypeError:
        pass
    try:
        return base64.standard_b64decode(s)
    except TypeError:
        raise TypeError('Could not decode as hex or base64')


@app.route('/redirect', methods=['GET', 'POST'])
def make_redirect_ipython():
    # Check if archive is in hex or base64
    archive = request.args.get('archive')
    decoded = decodeString(archive)
    print decoded

    return redirect('http://www.google.com', code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
