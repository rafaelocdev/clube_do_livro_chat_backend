from flask import Flask
from flask_socketio import SocketIO
from os import getenv
from datetime import datetime

app = Flask(__name__)

app.debug = True
app.config["SECRET_KEY"] = getenv("SECRET_KEY")

socket_io = SocketIO(app, cors_allowed_origins="*")


@socket_io.on("connect")
def test_connect():
    print("Client connected")


@socket_io.on("disconnect")
def test_disconnect():
    print("Client disconnected")


@socket_io.on("message")
def test_send_message(message, sender, reciever):
    print(100 * "#")
    print(f"{message=}")
    print(f"{sender=}")
    print(f"{reciever=}")
    print(f"{datetime.now()=}")
    print(100 * "#")


if __name__ == "__main__":
    socket_io.run(app, host="0.0.0.0", port=5000, debug=True)
