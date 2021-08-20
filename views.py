from main import app
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html", page_title="PSnoD")

@app.route("/predict")
def predict():
    return render_template("predict.html", page_tiel="PSnoD predict")