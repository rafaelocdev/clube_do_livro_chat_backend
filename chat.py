from flask import Flask
from flask_socketio import SocketIO, join_room
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.debug = True
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.config["JSON_SORT_KEYS"] = False

socket_io = SocketIO(app, cors_allowed_origins="*")


@socket_io.on("connect")
def test_connect():
    print("Client connected")


@socket_io.on("disconnect")
def test_disconnect():
    print("Client disconnected")


@socket_io.on("join_room")
def handle_join_room_event(data):
    app.logger.info(
        "{} has joined the room {} with {}".format(
            data["sender_id"], data["room_id"], data["receiver_id"]
        )
    )
    join_room(data["room_id"])


@socket_io.on("send_message")
def send_message(data):

    app.logger.info(
        "{} has sent message to the room {}: {}".format(
            data["sender_id"], data["room_id"], data["message_text"]
        )
    )

    data = {
        "room_id": data["room_id"],
        "sender_id": data["sender_id"],
        "message_text": data["message_text"],
        "created_at": data["created_at"],
    }

    socket_io.emit("receive_message", data, room=data["room_id"])


if __name__ == "__main__":
    socket_io.run(app, host="0.0.0.0", port=5001, debug=True)
