#client
import socket
from tkinter import *

def main():
    host = '127.0.0.1'
    port = 15000
    #int(input("Please enter the port number: "))
    client(host,port)
    

def client(host,port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))


    # #msg = client_socket.recv(1024)
    # #print(msg.decode("utf-8"))

    # username = input("Enter A Username: ")
    # client_socket.send(bytes(username, "utf-8"))
    # response = client_socket.recv(1024)
    # print(response.decode("utf-8"))

    # while True:
    #     message = input("Type here: ")
    #     client_socket.send(bytes(message, "utf-8"))
    #     if message == "stop;":
    #         client_socket.close()

    window = Tk()
    window.title("Chat Client")

    # Create a text field to display chat history
    chat_history = Text(window)
    chat_history.pack()
    chat_history.config(state=DISABLED)

    # Create a text field for user input
    user_input = Entry(window)
    user_input.bind("<Return>", lambda event: send_message(user_input, client_socket, chat_history))
    user_input.pack()

    window.mainloop()

def send_message(user_input, client_socket, chat_history):
    message = user_input.get()
    client_socket.send(bytes(message, "utf-8"))
    chat_history.config(state=NORMAL)
    chat_history.insert(END, "You: " + message + "\n")
    chat_history.config(state=DISABLED)
    user_input.delete(0, END)



    

    

main()