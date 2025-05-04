import socket, threading, pickle

game_state = {
    "ball": [400, 300],
    "ball_vel": [5, 5],
    "left_paddle": 250,
    "right_paddle": 250
}

clients = []

def handle_client(conn, addr, player_id):
    global game_state
    conn.send(pickle.dumps(player_id))  # Tell client its ID

    while True:
        try:
            data = pickle.loads(conn.recv(1024))
            if player_id == 0:
                game_state["left_paddle"] = data
            else:
                game_state["right_paddle"] = data

            # Ball movement (basic server-side physics)
            ball = game_state["ball"]
            vel = game_state["ball_vel"]
            ball[0] += vel[0]
            ball[1] += vel[1]

            if ball[1] <= 0 or ball[1] >= 600:
                vel[1] *= -1
            if ball[0] <= 0 or ball[0] >= 800:
                ball[0], ball[1] = 400, 300  # Reset

            # Send updated state to all clients
            for c in clients:
                c.send(pickle.dumps(game_state))

        except:
            break

# Stat Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('147.185.221.26', 56073))
server.listen(2)
print("Server started")

for i in range(2):
    conn, addr = server.accept()
    clients.append(conn)
    print(f"Player {i} connected from {addr}")
    thread = threading.Thread(target=handle_client, args=(conn, addr, i))
    thread.start()