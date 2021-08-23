import sys
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy, Model
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from flask import render_template
from flask import request
from flask import redirect
from flask import flash, url_for

app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

UPLOAD_FOLDER = "./user_file"
ALLOWED_EXTENSIONS = {'txt', "fasta", "fa"}

app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(app.root_path, "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = b"_5#y2LF4#d\xe9X\x00\xbe~Uq\xebX\xae\x81\x1fs\t\xb4\x99\xa3\x87\xec]/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

import views