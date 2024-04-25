#server
import socket
import threading
import rsa


clients = []

def main():
	host = '127.0.0.1'
	port = 15000
    #start the server
	serverTCP(host, port)
    
	
def serverTCP(host, port):
    #create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #bind the socket 
    server_socket.bind((host, port))
    
    #listen for incoming connections
    server_socket.listen(10)
    print(f"Server listening on {host}:{port}")

    while True:
        #wait for a connection
        conn, addr = server_socket.accept()

        #start thread to handle the client
        client_thread = threading.Thread(target=handleClients, args=(conn, addr))
        client_thread.start()
        

def handleClients(conn, addr):
    #generate a new RSA key pair
    public_key, private_key = rsa.newkeys(512)

    #send the public rsa key to the client
    conn.send(public_key.save_pkcs1())

    #receive public rsa key from client
    public_key_data = conn.recv(4096)
    cli_public_key = rsa.PublicKey.load_pkcs1(public_key_data)

    #encrypted username of client received
    encrypted_username = conn.recv(1024)
    username = rsa.decrypt(encrypted_username, private_key).decode("utf-8")

    print(f"Connection from {addr}|User: {username}")

    #send welcome message to client
    welcome_message = f"Welcome to the server, {username}!"
    encrypted_message = rsa.encrypt(welcome_message.encode(), cli_public_key)
    conn.send(encrypted_message)

    #store client connection and key
    clients.append((conn, cli_public_key))

    
    while True:
        #receive messages
        encrypted_message = conn.recv(1024)
        if not encrypted_message:
            break
        #decrypt
        message = rsa.decrypt(encrypted_message, private_key).decode("utf-8")
        print(f"{username}: {message}")

        # Broadcast the message to all connected clients
        broadcast_message = f"{username}: {message}"
        for client in clients:
            try:
                #try to send the message
                client[0].send(rsa.encrypt(broadcast_message.encode(), client[1]))
            except OSError:
                #if an error occurs, remove the client from the list
                clients.remove(client)

    conn.close()

main()