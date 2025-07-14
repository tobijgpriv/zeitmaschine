from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from threading import Lock
import logging
from enum import Enum

from zeitmaschine import zeitreise, standardbeleuchtung
from gpiozero import RotaryEncoder, Button

# GPIO Pins
pin_dt = 23
pin_clk = 18
pin_sw = 24

encoder = RotaryEncoder(a=pin_clk, b=pin_dt, max_steps=0)
button = Button(pin_sw)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
logging.basicConfig(level=logging.INFO)

# Zustände
class ZeitmaschinenStatus(Enum):
    IDLE = "idle"
    INITIALISIERT = "initialisiert"
    LAUFEND = "laufend"
    BEENDET = "beendet"
    ABGEBROCHEN = "abgebrochen"

# State-Controller
class ZeitmaschinenController:
    def __init__(self):
        self.actual_year = 2025
        self.target_year = 2025
        self.duration = 43200
        self.encoder_value = 0
        self.state = ZeitmaschinenStatus.IDLE
        self.lock = Lock()

    def set_target_year(self, year):
        with self.lock:
            self.target_year = int(year)
            self._update_state()

    def set_actual_year(self, year):
        with self.lock:
            self.actual_year = int(year)

    def set_duration(self, duration):
        with self.lock:
            self.duration = int(duration)
            self._update_state()

    def start(self):
        with self.lock:
            if self.duration > 0:
                self.state = ZeitmaschinenStatus.LAUFEND
                zeitreise()
            else:
                self.state = ZeitmaschinenStatus.IDLE

    def stop(self):
        with self.lock:
            if self.state == ZeitmaschinenStatus.LAUFEND:
                self.state = ZeitmaschinenStatus.ABGEBROCHEN
                standardbeleuchtung()

    def beendet(self):
        with self.lock:
            if self.state == ZeitmaschinenStatus.LAUFEND:
                self.state = ZeitmaschinenStatus.BEENDET
                standardbeleuchtung()

    def reset(self):
        with self.lock:
            self.__init__()
            standardbeleuchtung()

    def restart(self):
        with self.lock:
            self.state = ZeitmaschinenStatus.LAUFEND
            zeitreise()

    def _update_state(self):
        if self.duration > 0 and self.target_year != self.actual_year:
            self.state = ZeitmaschinenStatus.INITIALISIERT
        else:
            self.state = ZeitmaschinenStatus.IDLE

    def get_status(self):
        with self.lock:
            return {
                "state": self.state.value,
                "actual": self.actual_year,
                "year": self.target_year,
                "duration": self.duration,
                "start": self.state in [ZeitmaschinenStatus.LAUFEND],
                "running": self.state == ZeitmaschinenStatus.LAUFEND
            }

controller = ZeitmaschinenController()

def broadcast_status():
    logging.info(controller.get_status())
    socketio.emit('status_update', controller.get_status())

# Rotary Encoder Steuerung
def on_rotate():
    controller.encoder_value = encoder.steps * 10
    new_target = 2025 + controller.encoder_value
    controller.set_target_year(new_target)
    logging.info(f"Zieljahr geändert: {new_target}")
    broadcast_status()

def on_press():
    controller.encoder_value = 0
    encoder.steps = 0
    controller.start()
    logging.info("Zeitreise gestartet")
    broadcast_status()

encoder.when_rotated = on_rotate
button.when_pressed = on_press

# Routen
@app.route("/")
def index():
    return render_template("konsole.html")

@app.route("/anzeige")
def zeitanzeige():
    standardbeleuchtung()
    return render_template("zeitmaschine.html")

@app.route("/status")
def status():
    status_info = controller.get_status()
    logging.info(f"Status abgefragt: {status_info}")
    return jsonify(status_info)

@app.route("/start", methods=["POST"])
def start():
    year = request.form.get("year")
    duration = request.form.get("duration")
    if not year or not year.lstrip("-").isdigit():
        return "Ungültiges Jahr", 400
    try:
        controller.set_target_year(year)
        controller.set_duration(duration)
        controller.start()
        return "Zeitreise gestartet", 200
    except ValueError:
        return "Ungültige Dauer", 400

@app.route("/stop", methods=["POST"])
def stop():
    controller.stop()
    return jsonify({"status": "Zeitreise abgebrochen"})

@app.route("/beendet", methods=["POST"])
def beendet():
    controller.beendet()
    return jsonify({"status": "Zeitreise beendet"})

@app.route("/reset", methods=["POST"])
def reset():
    controller.reset()
    return "Reset OK", 200

@app.route("/restart", methods=["POST"])
def restart():
    controller.restart()
    return "Zeitreise neu gestartet", 200

@app.route("/set_actual_year", methods=["POST"])
def set_actual_year():
    year = request.form.get("year")
    if not year or not year.lstrip("-").isdigit():
        return "Ungültiges Jahr", 400
    controller.set_actual_year(year)
    return "Aktuelles Jahr gesetzt", 200

@app.route("/set_target_year", methods=["POST"])
def set_target_year():
    year = request.form.get("year")
    if not year or not year.lstrip("-").isdigit():
        return "Ungültiges Jahr", 400
    controller.set_target_year(year)
    return "Zieljahr gesetzt", 200

@app.route("/set_duration", methods=["POST"])
def set_duration():
    duration = request.form.get("duration")
    try:
        controller.set_duration(duration)
        broadcast_status()
        return "Dauer gesetzt", 200
    except ValueError:
        return "Ungültige Dauer", 400

# Hauptfunktion
if __name__ == "__main__":
    #app.run(host="0.0.0.0", debug=False)
    socketio.run(app, host="0.0.0.0", debug=False,allow_unsafe_werkzeug=True)
