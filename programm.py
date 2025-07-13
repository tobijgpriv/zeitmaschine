from zeitmaschine import zeitreise,standardbeleuchtung
from flask import Flask, render_template, request,jsonify
from threading import Lock
import logging

from gpiozero import RotaryEncoder, Button

pin_dt = 23
pin_clk = 18
pin_sw = 24

encoder = RotaryEncoder(a=pin_clk, b=pin_dt, max_steps=0)
button = Button(pin_sw)

#Start Task runOnPi with Strg+Alt+r
app = Flask(__name__)

current_actual_year = 2025
current_target_year = 2025
current_started = False
current_duration=20
current_running = False
current_encoder_value = 0
year_lock = Lock()

def on_rotate():
    global current_encoder_value
    current_encoder_value = encoder.steps*10
    current_target_year = 2025 + current_encoder_value
    logging.error(f"Counter value: {current_target_year}")

def on_press():
    global current_encoder_value
    current_encoder_value = 0
    encoder.steps = 0
    logging.error("Counter reset to 0")

encoder.when_rotated = on_rotate
button.when_pressed = on_press

@app.route('/start', methods=["POST"])
def zeitmaschine():
    if request.method == 'POST':
        year = request.form['year']
        duration = request.form['duration']
    if duration!=0:
        zeitreise()
    if not year or not year.lstrip("-").isdigit():
        return "Ungültige Eingabe", 400
    with year_lock:
        global current_target_year 
        global current_duration
        global current_running
        global current_started
        current_started = True
        current_running = int(duration) > 0
        current_target_year = int(year)
        try:
            current_duration = int(duration)
        except (TypeError, ValueError):
            current_duration = 20  # fallback
    return "Zeitreise gestartet", 200
    #return render_template('zeitmaschine.html', target_year=int(year))

@app.route("/set_duration", methods=["POST"])
def set_duration():
    global current_duration
    duration = request.form.get("duration")
    try:
        current_duration = int(duration)
        return "Dauer gesetzt", 200
    except (TypeError, ValueError):
        return "Ungültige Dauer", 400
    
@app.route("/status")
def status():
    with year_lock:
        if current_started:
            logging.error({"start": True, "year": current_target_year, "duration": current_duration, "running":current_running, "actual": current_actual_year})
            return jsonify({"start": True, "year": current_target_year, "duration": current_duration, "running":current_running, "actual": current_actual_year})
        else:
            logging.error({"start": False, "year": current_target_year, "duration": current_duration, "running":current_running, "actual": current_actual_year})
            return jsonify({"start": False, "year": current_target_year, "duration": current_duration, "running":current_running, "actual": current_actual_year})

@app.route("/anzeige")
def zeitanzeige():
    standardbeleuchtung()
    return render_template("zeitmaschine.html")  

@app.route("/set_actual_year", methods=["POST"])
def set_actual_year():
    global current_actual_year
    year = request.form.get("year")
    if not year or not year.lstrip("-").isdigit():
        return "Ungültiges Jahr", 400
    current_actual_year = int(year)
    return "Aktuelles Jahr gesetzt", 200    

@app.route("/set_target_year", methods=["POST"])
def set_target_year():
    global current_target_year
    year = request.form.get("year")
    if not year or not year.lstrip("-").isdigit():
        return "Ungültiges Jahr", 400
    current_target_year = int(year)
    return "Aktuelles Jahr gesetzt", 200 
    
@app.route("/reset", methods=["POST"])
def reset():
    standardbeleuchtung()
    global current_running
    current_running = False
    global current_target_year
    with year_lock:
        current_target_year = None
    return "Reset OK", 200

@app.route('/')
def index():
    return render_template('konsole.html')

@app.route("/stop", methods=["POST"])
def stop():
    global current_running
    current_running = False
    standardbeleuchtung()  
    return jsonify({"status": "ok"})



if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0")


    rotary = Rotary(pin_dt, pin_clk, pin_sw)
    value = 0
    logging.error(value)