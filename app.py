from flask import Flask, render_template, make_response, request
import cowsay
import io
from contextlib import redirect_stdout
import random

app = Flask('cowsay', template_folder='/home/q498620/projects/udacity/udacity-devops-capstone/templates')

SERVICE_VERSION = '0.0.1'

class UnknownSayerException(Exception):
    pass

def capture_say(what, who='cow'):

    if who == 'random':
        who = random.choice(cowsay.char_names)

    if who not in cowsay.char_names:
        raise UnknownSayerException(f'sayer {who} not known to me')

    sayer_call = getattr(cowsay, who)

    f = io.StringIO()
    with redirect_stdout(f):
        sayer_call(what)
    return f.getvalue()

@app.route('/')
def index():
    resp_text = capture_say(f'COWSAY service {SERVICE_VERSION}')
    resp = make_response(render_template('index.html', almighty_content=resp_text), 200)
    return resp

@app.errorhandler(404)
def not_found(error):

    resp_text = capture_say("404! The path '{}' was not found on this server.".format(request.path), who='random')
    resp = make_response(render_template('404.html', almighty_content=resp_text), 404)
    return resp

app.run(port=8080)