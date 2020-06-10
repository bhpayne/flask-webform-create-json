#!/usr/bin/env python3

import json
import os
import random

# https://docs.python.org/3/howto/logging.html
import logging
# https://gist.github.com/ibeex/3257877
from logging.handlers import RotatingFileHandler

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
# https://nickjanetakis.com/blog/fix-missing-csrf-token-issues-with-flask
from flask_wtf import FlaskForm, CSRFProtect, Form  # type: ignore

from wtforms import StringField, validators, FieldList, FormField, IntegerField, RadioField, PasswordField, SubmitField, BooleanField  # type: ignore


# https://hplgit.github.io/web4sciapps/doc/pub/._web4sa_flask004.html
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
    flash,
    jsonify,
    Response,
)

from config import (
    Config,
)  # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

import compute


# https://nickjanetakis.com/blog/fix-missing-csrf-token-issues-with-flask
csrf = CSRFProtect()

app = Flask(__name__, static_folder="static")
app.config.from_object(
    Config
)  # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

# https://nickjanetakis.com/blog/fix-missing-csrf-token-issues-with-flask
csrf.init_app(app)


log_size = 10000000
# https://gist.github.com/ibeex/3257877
handler_debug = RotatingFileHandler(
        "logs/flask_critical_and_error_and_warning_and_info_and_debug.log",
        maxBytes=log_size,
        backupCount=2,
    )
handler_debug.setLevel(logging.DEBUG)
handler_info = RotatingFileHandler(
        "logs/flask_critical_and_error_and_warning_and_info.log",
        maxBytes=log_size,
        backupCount=2,
    )
handler_info.setLevel(logging.INFO)
handler_warning = RotatingFileHandler(
        "logs/flask_critical_and_error_and_warning.log",
        maxBytes=log_size,
        backupCount=2,
    )

handler_warning.setLevel(logging.WARNING)

# https://docs.python.org/3/howto/logging.html
logging.basicConfig(
        handlers=[handler_debug, handler_info, handler_warning],
        level=logging.DEBUG,
        format="%(asctime)s|%(filename)-13s|%(levelname)-5s|%(lineno)-4d|%(funcName)-20s|%(message)s"  # ,
)

logger = logging.getLogger(__name__)
# http://matplotlib.1069221.n5.nabble.com/How-to-turn-off-matplotlib-DEBUG-msgs-td48822.html
# https://github.com/matplotlib/matplotlib/issues/14523
logging.getLogger("matplotlib").setLevel(logging.WARNING)


class MyInputForm(FlaskForm):
    logger.info("[trace]")
    #    r = FloatField(validators=[validators.InputRequired()])
    #    r = FloatField()
    name = StringField(
        "a string", validators=[validators.InputRequired(), validators.Length(max=1000)]
    )



@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    """
    the index is a static page intended to be the landing page for new users
    >>> index()
    """
    trace_id = str(random.randint(1000000, 9999999))
    logger.info("[trace page start " + trace_id + "]")

    webform = MyInputForm(request.form)

    if request.method == "POST":  #  and webform.validate():
        logger.debug("request.form = %s", request.form)

    list_of_opts = ['cow', 'dog', 'rabbit']

    logger.info("[trace page end " + trace_id + "]")
    return render_template("index.html", 
                           webform=webform,
                           list_of_opts=list_of_opts)



if __name__ == "__main__":
    # this is only applicable for flask (and not gunicorn)
    app.run(debug=True, host="0.0.0.0")
