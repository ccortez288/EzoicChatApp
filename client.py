"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import tkinter.font as tkFont
from tkinter import RAISED

"""
This section handles all of the sending and receiving protocols
"""

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            messages.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        chat_gui.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()
"""
This section is where the GUI is initialized 
"""
chat_gui = tkinter.Tk()
chat_gui.title("Ezoic Chat App")
chat_gui.geometry('700x420')
chat_gui.configure(bg='lightblue')
var = tkinter.StringVar()
var = 'Ezoic Chat App'
label = tkinter.Label(chat_gui, text='Ezoic Chat App')
label.config(width=200, bg='lightblue')
label.config(font=("Courier", 44))
label.pack()
f = tkFont.Font(label, label.cget("font"), weight='bold')
f.configure(underline = True)
label.configure(font=f)

"""
This section contains the textbox where messages are received
"""
messages_frame = tkinter.Frame(chat_gui)
my_msg = tkinter.StringVar()  # For the messages to be sent.
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
messages = tkinter.Listbox(messages_frame, height=15, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
messages.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages.pack()
messages_frame.pack()

"""
This section contains the box for text entry where messages are written and sent from
"""
text_entry = tkinter.Entry(chat_gui, width=50, textvariable=my_msg, font=('default', 12))
text_entry.bind("<Return>", send)
text_entry.pack()
send_button = tkinter.Button(chat_gui, text="Send", command=send)
send_button.pack()
chat_gui.protocol("WM_DELETE_WINDOW", on_closing)

"""
This section contains the connection to the websocket, and launches another thread to receive
messages on. Here is where the eventloop for the GUI is launched as well. Home IP is set as default. 
Chat app only works on local machine with two different instances launched. 
"""
HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.