import tkinter as tk #gui library
import socket
import threading
import queue

def connect():
    global client_socket
    
    # Get the IP address and port number from the text boxes
    ip_address = ip_textbox.get()
    port_number = int(port_textbox.get())
    
    # Create a socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_address, port_number))
    print("Connected to server")
    
    # Start the receive and send threads
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    send_thread = threading.Thread(target=send)
    send_thread.start()

def receive():
    # Receive data from the server and Sending it to the Sending textbox
    while True:
        data = client_socket.recv(1024).decode("utf-8")
        if not data:
            break
        Receiving_textbox.configure(state=tk.NORMAL)
        Receiving_textbox.delete("1.0", tk.END)
        Receiving_textbox.insert(tk.END, data)
        Receiving_textbox.configure(state=tk.DISABLED)

def send():
    # Send data entered in the Sending textbox to the server
    while True:
        data = Sending_queue.get()
        if data == "quit":
            client_socket.send(data.encode("utf-8"))
            client_socket.close()
            break
        client_socket.send(data.encode("utf-8"))

def send_message():
    # Get the text from the Sending textbox and add it to the Sending queue
    data = Sending_textbox.get("1.0", "end-1c")
    Sending_queue.put(data)
    
    # Clear the Sending textbox
    Sending_textbox.delete("1.0", tk.END)


def close():
    client_socket.close()
    print("Disconnected from the Server")
    root.destroy()
    exit()

root = tk.Tk()

root.title('Instant LAN Messenger Client')

root.geometry('690x450')

# Create the "Enter IP and Port" label
enter_label = tk.Label(root, text="Enter IP and Port:")

# Create the IP address label and text box
ip_label = tk.Label(root, text="IP Address:")
ip_textbox = tk.Entry(root)

# Create the port number label and text box
port_label = tk.Label(root, text="Port Number:")
port_textbox = tk.Entry(root)

# Create the Receiving label and text box
Receiving_label = tk.Label(root, text="Receiving")
Receiving_textbox = tk.Text(root, height=6.5, width=60)

# Create the Sending label and text box
Sending_label = tk.Label(root, text="Sending")
Sending_textbox = tk.Text(root, height=6.5, width=60)

# Create the connect button
connect_button = tk.Button(root, text="Connect", command=connect)

# Create the send button
send_button = tk.Button(root, text="Send", command=send_message)


button = tk.Button(root, text = 'Terminate session', command = close)
button.grid(row=5, column=2)

# Place the labels and text boxes in the window
enter_label.grid(row=0, column=0, columnspan=2)
ip_label.grid(row=1, column=0)
ip_textbox.grid(row=1, column=1)
port_label.grid(row=2, column=0)
port_textbox.grid(row=2, column=1)
Receiving_label.grid(row=3, column=0, pady=10)
Receiving_textbox.grid(row=3, column=1, pady=10)
Sending_label.grid(row=4, column=0, pady=10)
Sending_textbox.grid(row=4, column=1, pady=10)

# Place the connect and send buttons in the last row
connect_button.grid(row=2, column=2)
send_button.grid(row=5, column=1,padx=10,pady=10)

# Create a socket object and set it to None
client_socket = None

# Create a queue to hold Sending messages
Sending_queue = queue.Queue()

root.mainloop()
