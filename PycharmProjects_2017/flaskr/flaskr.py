import time
import secrets
import logging
from flask import Flask, request, session, escape, render_template, redirect, url_for, send_file, send_from_directory

app = Flask(__name__)


'''
@app.route('/')
def index():
    if 'authorized' in session and session['authorized'] is True:
        return 'You are Logged in'
    else:
        return 'You are not logged in'
'''


@app.route('/')
def index():
    return render_template('images.html',
                           img_1='/images/10001.jpg',
                           img_2='/images/10002.jpg',
                           img_3='/images/10003.jpg',
                           img_4='/images/10004.jpg')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin888':
            session['authorized'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error_msg='Invalid Login'), 401
    else:
        raise NotImplementedError


@app.route('/images/<uid>')
def images(uid):
    return send_from_directory('images', uid, mimetype='image/jpeg')


def init_logging():
    logging.basicConfig(format='[%(levelname)s] %(asctime)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger('werkzeug')

    def log(self, type, message, *args):
        getattr(logger, type)('%s - %s' % (self.address_string(), message % args))

    from werkzeug.serving import WSGIRequestHandler
    WSGIRequestHandler.log = log


def run_server():
    app.secret_key = b'10086'  # app.secret_key = secrets.randbits(256)
    app.run(host='127.0.0.1', port=8000)


if __name__ == '__main__':
    init_logging()
    run_server()
