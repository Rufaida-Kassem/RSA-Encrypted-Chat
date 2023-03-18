import socket

client_socket = socket.socket()
port = 12345
client_socket.connect(('127.0.0.1',port))

#recieve connection message from server
recv_msg = client_socket.recv(1024)
print (recv_msg)

#send user details to server
# send_msg is a bytes-like object and it should be in format [#username], get it from user
send_msg = input("Enter your username in format [#username] ")
# convert send_msg to bytes-like object
send_msg_bytes = send_msg.encode('utf-8')
client_socket.send(send_msg_bytes)


#receive and send message from/to different user/s

while True:
    recv_msg = client_socket.recv(1024)
    print (recv_msg)
    send_msg = input("Send your message in format [@user:message] ")
    if send_msg == 'exit':
        break;
    else:
        send_msg_bytes = send_msg.encode('utf-8')
        client_socket.send(send_msg_bytes)


client_socket.close()
