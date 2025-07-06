from zeitmaschine import drei,vier,strob,drehlicht
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('zeitmaschine.html')



if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="0.0.0.0")