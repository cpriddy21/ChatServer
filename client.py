#client
import socket
import threading
from tkinter import *
import datetime
import time
import ssl


def main():
    host = '127.0.0.1'
    port = 15000
    #int(input("Please enter the port number: "))
    client(host,port)
    

def client(host,port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client_socket.connect((host, port))

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
    user_input.bind("<Return>", lambda event: send_message(user_input, client_socket, chat_history))
    user_input.bind("<FocusIn>", lambda event: handle_focus(event, user_input))
    user_input.pack()
    

    thread = threading.Thread(target=update_chat, args=(client_socket, chat_history))
    thread.start()

    window.mainloop()
    

    # while True:
    #     message = input()
    #     client_socket.send(bytes(message, "utf-8"))
    #     message = user_input.get()
    #     chat_history.config(state=NORMAL)
    #     chat_history.insert(END, "User: " + message + "\n")
    #     chat_history.config(state=DISABLED)
    #     if message == "stop;":
    #         client_socket.close()

def handle_focus(event, user_input):
    if user_input.get() == 'Type a message...':
        user_input.delete(0, END)  # Clear the input box when it's focused

def update_chat(client_socket,chat_history):
    while True:
        msg = client_socket.recv(1024).decode("utf-8")
        print(msg)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"[{timestamp}] {msg}"
        chat_history.config(state=NORMAL)
        chat_history.insert(END, msg + "\n")
        chat_history.config(state=DISABLED)
        with open('chatlog.txt', 'a') as file:
            # Write some text to the file
            file.write(msg + "\n")



def send_message(user_input, client_socket, chat_history):
    message = user_input.get()
    time.sleep(0.1)
    client_socket.send(bytes(message, "utf-8"))
    # chat_history.config(state=NORMAL)
    # chat_history.insert(END, "You: " + message + "\n")
    # chat_history.config(state=DISABLED)
    user_input.delete(0, END)
    user_input.bind("<FocusIn>", lambda event: handle_focus(event, user_input))  # Rebind focus event
    


def close_window(client_socket, window):
    client_socket.close()  # Close the socket connection
    window.quit()  # Quit the Tkinter application
    

    

main()