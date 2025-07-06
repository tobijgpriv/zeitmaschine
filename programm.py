from zeitmaschine import drei,vier,strob,drehlicht
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('zeitmaschine.html')



drei(1)