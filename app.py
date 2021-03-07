from flask import Flask, render_template, make_response, request
import cowsay
import io
from contextlib import redirect_stdout
import random

import pathlib
import os.path as path

app = Flask('cowsay', template_folder=path.join(pathlib.Path(__file__).parent.absolute(), 'templates'))

SERVICE_VERSION = '0.0.1'

class UnknownSayerException(Exception):
    pass

def capture_say(message, speaker='cow'):

    if speaker == 'random':
        speaker = random.choice(cowsay.char_names)

    if speaker not in cowsay.char_names:
        raise UnknownSayerException(f"sayer '{speaker}' not known to me")

    speaker_say = getattr(cowsay, speaker)

    f = io.StringIO()
    with redirect_stdout(f):
        speaker_say(message)
    return f.getvalue()

def build_err_40x(message, speaker='random', http_status=404):
    resp_text = capture_say(message, speaker=speaker)
    resp = make_response(render_template('40x.html', almighty_content=resp_text, http_status=http_status), http_status)
    return resp

def build_response(message, speaker='cow'):
    
    try:
        resp_text = capture_say(message, speaker=speaker)
        resp = make_response(render_template('index.html', almighty_content=resp_text), 200)
        return resp
        
    except UnknownSayerException as err:
        return build_err_40x(str(err))

@app.route('/')
def index():
    
    return build_response(f'COWSAY service {SERVICE_VERSION}')

@app.route('/say', methods=['POST'])
def say():

    try:
        message = request.form['message'],
        speaker = request.form['speaker']
        return build_response(message, speaker=speaker)
    except Exception as err:
        return build_err_40x(str(err), http_status=400)

@app.route('/speakers')
def speakers():
    cowsay_speakers = '\n'.join(cowsay.char_names)

    return build_response(f'available speakers:\n\n{cowsay_speakers}')

@app.errorhandler(404)
def not_found(error):

    return build_err_40x("404! The path '{}' was not found on this server.".format(request.path))

app.run(port=8080)