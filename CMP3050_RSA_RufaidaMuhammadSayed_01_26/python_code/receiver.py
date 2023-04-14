# this is the receiver program

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from rsa import *
import time


receiver = socket(AF_INET, SOCK_STREAM)
host = '127.0.0.1'
port = 33000

sender_name = None
sender_e = None
sender_n = None

e = None
d = None
n = None


# hand shake with sender
def hand_shake():
    # send message to sender
    send_msg = input("Enter your username\n")

    # receive message from sender
    global sender_name
    sender_name = receiver.recv(1024).decode('utf-8')
    
    send_msg_bytes = send_msg.encode('utf-8')
    receiver.send(send_msg_bytes)
    
    # recieve the public key from sender
    global sender_e, sender_n
    sender_e, sender_n = receiver.recv(1024).decode('utf-8').split(',')
    sender_e = int(sender_e)
    sender_n = int(sender_n)
    
    # send the public key to sender
    send_msg = str(e) + ',' + str(n)
    receiver.send(send_msg.encode('utf-8'))
    
    # start chat by starting two threads for sending and receiving messages
    send_msg_thread = Thread(target=send_message)
    receive_message_thread = Thread(target=receive_message)
    send_msg_thread.start()
    receive_message_thread.start()
    send_msg_thread.join()
    receive_message_thread.join()
    
    
# receive message from sender
def receive_message():
    recv_msg = ''
    while True:
        # concat the message with the previous message
        _end = receiver.recv(1024).decode('utf-8')
        if _end == '\n':
            print (sender_name, ": ", recv_msg, flush=True)  
            recv_msg = ''
        else:
            recv_msg += decrypt(int(_end), d, n)


# send message to sender
def send_message():
    while True:
        send_msg = input().lower()
        encrypted_msg = encrypt(send_msg, sender_e, sender_n)
        for block in encrypted_msg:
            # send the block to sender
            block = str(block)
            receiver.send(block.encode('utf-8'))
            # sleep for 0.002 seconds
            time.sleep(0.002)
        # send the end of message to sender
        receiver.send('\n'.encode('utf-8'))
            
# main function
if __name__ == "__main__":
    
    number_of_bits = int(input("Enter number of bits for key generation: "))
    while True:
        try:
            # generate the public key and private key
            e, d, n = generate_keys(number_of_bits)
            
            # if generated successfully, break the loop
            break
        except:
            continue

    receiver.connect((host, port))
    # receive welcome message from sender
    _ = receiver.recv(1024).decode('utf-8')

    hand_shake()
    receiver.close()