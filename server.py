#server
import socket
import threading

clients = []

def main():
	host = '127.0.0.1'
	port = 15000
	serverTCP(host, port)
    
	
def serverTCP(host, port):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to a specific address and port
    server_socket.bind((host, port))
    
    # Listen for incoming connections
    server_socket.listen(10)
    print(f"Server listening on {host}:{port}")

    while True:
        # Wait for a connection
        conn, addr = server_socket.accept()
        clients.append(conn)

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handleClients, args=(conn, addr))
        client_thread.start()
        

def handleClients(conn, addr):
    username = conn.recv(1024).decode("utf-8")
    print(f"Connection from {addr}|User: {username}")
    conn.send(bytes(f"Welcome to the server, {username}!", "utf-8"))

    while True:
        message = conn.recv(1024).decode("utf-8")
        if not message:
            break
        print(f"{username}: {message}")

        # Broadcast the message to all connected clients
        broadcast_message = f"{username}: {message}"
        for client in clients:
            try:
                # Try to send the message
                client.send(bytes(broadcast_message, "utf-8"))
            except OSError:
                # If an error occurs, remove the client from the list
                clients.remove(client)

    conn.close()

main()