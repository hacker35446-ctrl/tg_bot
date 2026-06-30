from flask import Flask
import threading

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "OK"

def run_server():
    app.run(host="0.0.0.0", port=10000)

def start_server_thread():
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()