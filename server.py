import tkinter as tk #gui library
import socket
import threading
import queue

def start_server():
    global server_socket, client_socket
    
    # Get the port number from the text box
    port_number = int(port_textbox.get())
    
    # Create a socket and bind it to the port number
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port_number))
    server_socket.listen(1)
    print("Server started")
    
    # Accept a client connection
    client_socket, address = server_socket.accept()
    print("Connected to client at", address)
    
    # Start the receive and send threads
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    send_thread = threading.Thread(target=send)
    send_thread.start()

def receive():
    # Receive data from the client and sending it to the sending textbox
    while True:
        data = client_socket.recv(1024).decode("utf-8")
        if not data:
            break
        Recieving_textbox.configure(state=tk.NORMAL)
        Recieving_textbox.delete("1.0", tk.END)
        Recieving_textbox.insert(tk.END, data)
        Recieving_textbox.configure(state=tk.DISABLED)

def send():
    # Send data entered in the sending textbox to the client
    while True:
        data = sending_queue.get()
        if data == "quit":
            client_socket.send(data.encode("utf-8"))
            client_socket.close()
            server_socket.close()
            break
        client_socket.send(data.encode("utf-8"))

def send_message():
    # Get the text from the sending textbox and add it to the sending queue
    data = sending_textbox.get("1.0", "end-1c")
    sending_queue.put(data)
    
    # Clear the sending textbox
    sending_textbox.delete("1.0", tk.END)

def close():
    # Close the client socket and server socket
    client_socket.close()
    server_socket.close()
    print("Disconnected to the Client")
    root.destroy()
    exit()

root = tk.Tk()

root.title('Instant LAN Messenger Server')

root.geometry('690x450')

# Create the "Enter Port" label
enter_label = tk.Label(root, text="Enter Port:")

# Create the port number label and text box
port_label = tk.Label(root, text="Port Number:")
port_textbox = tk.Entry(root)

# Create the Recieving label and text box
Recieving_label = tk.Label(root, text="Recieving")
Recieving_textbox = tk.Text(root, height=6.5, width=60)

# Create the sending label and text box
sending_label = tk.Label(root, text="Sending")
sending_textbox = tk.Text(root, height=6.5, width=60)

# Create the start button
start_button = tk.Button(root, text="Start Listening", command=start_server)

# Create the send button
send_button = tk.Button(root, text="Send", command=send_message)


button = tk.Button(root, text = 'Terminate session', command = close)
button.grid(row=5, column=2)

# Place the labels and text boxes in the window
enter_label.grid(row=0, column=0, columnspan=2)
port_label.grid(row=1, column=0)
port_textbox.grid(row=1, column=1)
Recieving_label.grid(row=2, column=0, pady=10)
Recieving_textbox.grid(row=2, column=1, pady=10)
sending_label.grid(row=3, column=0, pady=10)
sending_textbox.grid(row=3, column=1, pady=10)

# Place the start and send buttons in the last row
start_button.grid(row=1, column=2, pady=10)
send_button.grid(row=5, column=1, pady=10)

# Create a socket object and set it to None
server_socket = None
client_socket = None

# Create a queue to hold sending messages
sending_queue = queue.Queue()

root.mainloop()
