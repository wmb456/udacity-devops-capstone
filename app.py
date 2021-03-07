'''
provides cowsay web service
'''
import io
import random
import pathlib
import os.path as path
from contextlib import redirect_stdout

from flask import Flask, render_template, make_response, request
import cowsay

current_path = pathlib.Path(__file__).parent.absolute()
template_folder = path.join(current_path, 'templates')
app = Flask('cowsay', template_folder=template_folder)

SERVICE_VERSION = '0.0.1'


class UnknownSayerException(Exception):
    '''
    thrown on a unknown cowsay speaker
    '''

def capture_say(message, speaker='cow'):
    '''
    capture the output of cowsay and return it as string
    '''

    if speaker == 'random':
        speaker = random.choice(cowsay.char_names)

    if speaker not in cowsay.char_names:
        raise UnknownSayerException(f"sayer '{speaker}' not known to me")

    speaker_say = getattr(cowsay, speaker)

    capture = io.StringIO()
    with redirect_stdout(capture):
        speaker_say(message)
    return capture.getvalue()


def build_err_40x(message, speaker='random', http_status=404):
    '''
    build a cowsay-ized 40x error response message
    '''

    resp_text = capture_say(message, speaker=speaker)
    resp = make_response(render_template('40x.html',
                                         almighty_content=resp_text,
                                         http_status=http_status),
                         http_status)
    return resp


def build_response(message, speaker='cow'):
    '''
    build a cowsay-ized response message with status 200
    '''

    try:
        resp_text = capture_say(message, speaker=speaker)
        resp = make_response(render_template(
            'index.html', almighty_content=resp_text), 200)
        return resp

    except UnknownSayerException as err:
        return build_err_40x(str(err))


@app.route('/')
def index():
    '''
    service root endpoint, delivers cowsay-ized service version
    '''
    return build_response(f'COWSAY service {SERVICE_VERSION}')


@app.route('/say', methods=['POST'])
def say():
    '''
    /say endpoint delivers cowsay-ized _message_ with given _speaker_
    only accepts http POST with form properties _message_ and _speaker_
    '''

    try:
        message = request.form['message']
        speaker = request.form['speaker']
        return build_response(message, speaker=speaker)
    except KeyError as err:
        return build_err_40x(str(err), http_status=400)


@app.route('/speakers')
def speakers():
    '''
    /speakers endpoint delivers a cowsay-ized list of available speakers
    '''
    cowsay_speakers = '\n'.join(cowsay.char_names)

    return build_response(f'available speakers:\n\n{cowsay_speakers}')


@app.errorhandler(404)
def not_found(error):
    '''
    basic 404 error handler providing cowsay-ized 404 error page using a random speaker
    '''
    _ = error
    return build_err_40x("404! The path '{}' was not found on this server.".format(request.path))


app.run(port=8080)
