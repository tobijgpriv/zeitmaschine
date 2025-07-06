from zeitmaschine import drei,vier,strob,drehlicht,zeitreise,standardbeleuchtung
from flask import Flask, render_template, request,jsonify
from threading import Lock

app = Flask(__name__)

current_target_year = None
year_lock = Lock()

@app.route('/start', methods=["POST"])
def zeitmaschine():
    zeitreise()
    if request.method == 'POST':
        year = request.form['year']
    if not year or not year.lstrip("-").isdigit():
        return "Ungültige Eingabe", 400
    with year_lock:
        app.logger.error("Debug" + year)
        global current_target_year 
        current_target_year = int(year)
    return "Zeitreise gestartet", 200
    #return render_template('zeitmaschine.html', target_year=int(year))

@app.route("/status")
def status():
    app.logger.error(current_target_year)
    print(current_target_year)
    with year_lock:
        if current_target_year is not None:
            return jsonify({"start": True, "year": current_target_year})
        else:
            return jsonify({"start": False})

@app.route("/anzeige")
def zeitanzeige():
    return render_template("zeitmaschine.html")      
    
@app.route("/reset", methods=["POST"])
def reset():
    global current_target_year
    with year_lock:
        current_target_year = None
    return "Reset OK", 200

@app.route('/')
def index():
    return render_template('konsole.html')

@app.route("/stop", methods=["POST"])
def stop():
    standardbeleuchtung()  # <-- Diese Funktion wird am Ende aufgerufen
    return jsonify({"status": "ok"})



if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0")