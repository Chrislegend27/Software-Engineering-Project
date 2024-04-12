import threading 
import socket

nickname = input("Choose a nickname: ")

host = '18.1.1.1'
port = 20_000 #Port for server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Creating client

client.connect((host, port))

def receive(): #Function in order to receive the messages sent from the server and define a nickname
    while True: #Constantly listening for server message
        try:
            message = client.recv(1024).decode('ascii') #receives a message from the server and decodes it
            if message == 'NICK': #Checks to see if asking for nickname
                client.send(nickname.encode('ascii')) #Sends the nickname you chose as your nickname to server
            else:
                #Normal case: prints any messages received from server
                print(message) 
        except: #Checks to see if there was an error then forces the client out the server if there was
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()