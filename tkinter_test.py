from tkinter import *
from tkinter import ttk

window = Tk()
window.title("Chat Client")

# Create a text field to display chat history
chat_history = Text(window)
chat_history.pack()
chat_history.config(state=DISABLED)

# Create a text field for user input
user_input = Entry(window)
user_input.bind("<Return>", lambda event: send_message(user_input, chat_history))
user_input.pack()

style = ttk.Style()
style.theme_use('clam')

label = ttk.Label(window, text="Fancy Label", bg="purple", fg="white", font=("Helvetica", 16, "bold"))
label.pack()

button = ttk.Button(window, text="Click Me")
button.pack()


window.mainloop()

def send_message(user_input, chat_history):
    message = user_input.get(text='Type a message...')
    
    chat_history.config(state=NORMAL)
    chat_history.insert(END, "You: " + message + "\n")
    chat_history.config(state=DISABLED)
    user_input.delete(0, END)
    with open('output_test'+ '' +'.txt', 'a') as file:
            # Write some text to the file
            file.write(message + "\n")