import sys
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy, Model
from flask_bootstrap import Bootstrap

app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'
app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(app.root_path, "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"]=b"_5#y2LF4#d\xe9X\x00\xbe~Uq\xebX\xae\x81\x1fs\t\xb4\x99\xa3\x87\xec]/"
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

import views