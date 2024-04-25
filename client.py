#client
import socket
import threading
from tkinter import *
from tkinter import ttk
import sv_ttk
import datetime
import time
import rsa



def main():
    host = '127.0.0.1'
    port = 15000
    #initialize client
    client(host,port)
    


def client(host,port):
    #generate RSA key pair
    public_key, private_key = rsa.newkeys(512)

    #create socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    #send the client's public rsa key to the server
    client_socket.send(public_key.save_pkcs1())

    #receive the public rsa key from the server
    public_key_data = client_socket.recv(4096)
    ser_public_key = rsa.PublicKey.load_pkcs1(public_key_data)

    #create chat window
    window = Tk()
    window.title("Chat Client")
    
    #stop script running when the chat window is closed
    window.bind("<Destroy>", lambda event: close_window(client_socket, window))

    #create a text field to display chat history
    chat_history = Text(window)
    chat_history.pack()
    chat_history.config(state=DISABLED)

    #create a text field for user input
    user_input = Entry(window)
    user_input.insert(0,'Type your username: ')
    username = {'value': ''}  #use a dictionary to hold the username
    user_input.bind("<Return>", lambda event: send_message(user_input, client_socket, chat_history, ser_public_key,username))
    user_input.bind("<Key>", lambda event: clear_textbox(event, user_input)) 
    user_input.pack()
    
    #thread to update chat history
    thread = threading.Thread(target=update_chat, args=(client_socket, chat_history, private_key,username))
    thread.start()

    window.mainloop()
    


def clear_textbox(event, user_input):
    if user_input.get() == 'Type a message...' or user_input.get() == 'Type your username: ' :
        user_input.delete(0, END)  # Clear the input box when it's focused
    



#updates the display of chat messages via messages from server
def update_chat(client_socket,chat_history, private_key,username):
    while True:
        #receive message from server
        encrypted_message = client_socket.recv(1024)
        #decrypt server message with client private key
        msg = rsa.decrypt(encrypted_message, private_key).decode("utf-8")
        
        #display
        print(msg)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"[{timestamp}] {msg}"

        #add to chat_history (what is displayed in the window)
        chat_history.config(state=NORMAL)
        chat_history.insert(END, msg + "\n")
        chat_history.config(state=DISABLED)

        #write to chatlog.txt
        with open(f'chatlog_{username["value"]}.txt', 'a') as file:
            # Write some text to the file
            file.write(msg + "\n")



#send a message to the server using rsa encryption, server public key
def send_message(user_input, client_socket, chat_history, ser_public_key, username):
    message = user_input.get()

    #if the username has not been saved yet, save it
    if username["value"] == '':
        un = message.strip()
        username["value"] = un  #save the username for later use
    
    encrypted_message = rsa.encrypt(message.encode(), ser_public_key)
    client_socket.send(encrypted_message)
    user_input.delete(0, END)
    user_input.insert(0,'Type a message...')
    
    user_input.bind("<Key>", lambda event: clear_textbox(event, user_input)) 
    


def close_window(client_socket, window):
    client_socket.close()  #close the socket connection
    window.quit()  #quit the Tkinter application
    

    

main()