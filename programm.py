from zeitmaschine import drei,vier,strob,drehlicht,zeitreise,standardbeleuchtung
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/zeitmaschine', methods=["POST"])
def zeitmaschine():
    #year = request.form.get("year")
    if request.method == 'POST':
        year = request.form['year']
    if not year or not year.isdigit():
        return "Ungültige Eingabe", 400
    return render_template('zeitmaschine.html', target_year=int(year))

@app.route('/')
def index():
    return render_template('konsole.html')

@app.route("/stop", methods=["POST"])
def stop_route():
    standardbeleuchtung()  # <-- Diese Funktion wird am Ende aufgerufen
    return jsonify({"status": "stopped"})



if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0")