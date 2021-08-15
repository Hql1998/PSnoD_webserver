from flask import Flask
from flask_sqlalchemy import SQLAlchemy, Model
import sys
import os

app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'
app.config["SQLALCHEMY_DATABASE_URI"] = prefix + os.path.join(app.root_path, "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

import views