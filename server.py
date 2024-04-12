import threading
import socket

host = '0.0.0.0'  # References to the computer's local host
port = 20_000  # Port for server

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))  # Binds server to local host at the port number
server.listen()

clients = []  # List to keep track of clients
nicknames = []  # List to keep track of client nicknames

def broadcast(message):  # Loops through all clients and sends message
    for client in clients:
        client.send(message)

def handle(client):  # This function handles a client, broadcasting messages and removing them if errors occur
    while True:
        try:
            message = client.recv(1024)  # Receives message of 1024 bytes size
            broadcast(message)  # Broadcasts this message
        except:
            index = clients.index(client)  # Gets the index of the client that failed
            clients.remove(client)  # Removes the client from the list
            client.close()  # Closes client connection
            nickname = nicknames[index]  # Gets the corresponding client nickname
            broadcast(f'{nickname} left the chat!'.encode('ASCII'))  # Broadcasts who left the chat
            nicknames.remove(nickname)  # Removes the nickname from the list
            break

def receive():
    while True:  # Accepting clients indefinitely
        client, address = server.accept()  # Accepts a connection
        print(f"Connected with {str(address)}")  # Prints the address that was connected

        client.send("NICK".encode("ascii"))  # Asks the client for their nickname
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode("ascii"))
        client.send("Connected to the server!".encode("ascii"))  # Fixed typo here from 'ecnode' to 'encode'

        thread = threading.Thread(target=handle, args=(client,))  # Fixed typo here from 'threading.thread' to 'threading.Thread'
        thread.start()

print("Server is listening....")
receive()
