from flask import Flask, request, render_template
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

clients = []

@app.route('/receiver')
def index():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def receive_post():
    data = request.data  # Get the raw request data
    print(data)  # Print it to the console

    # Notify all connected clients with the received data
    for client in clients:
        client.send(data.decode('utf-8'))  # Decode bytes to string

    return {"message": "Data received!"}, 200

@sock.route('/ws')
def websocket(ws):
    clients.append(ws)  # Add the new client to the list
    try:
        while True:
            msg = ws.receive()  # Keep the connection open
            if msg is None:
                break
    finally:
        clients.remove(ws)  # Remove the client when disconnected

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
