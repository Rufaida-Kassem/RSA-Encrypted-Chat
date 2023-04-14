# this script is used to chat with the receiver.py script
# this script is used to send messages to the receiver.py script

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from rsa import *
import time



HOST = ''
PORT = 33000
ADDR = (HOST, PORT)
sender = socket(AF_INET, SOCK_STREAM)
sender.bind(ADDR)


receiver_name = None
receiver_e = None
receiver_n = None

e = None
d = None
n = None



# accept incoming connection from receiver
def accept_incoming_connections():
    while True:
        receiver, receiver_address = sender.accept()
        print("%s:%s has connected." % receiver_address)
        receiver.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        Thread(target=hand_shake, args=(receiver,)).start()
        
        
# start hand shaking with receiver
def hand_shake(receiver):
    # send message to receiver
    send_msg = input("Enter your username\n")
    send_msg_bytes = send_msg.encode('utf-8')
    receiver.send(send_msg_bytes)
    
    # recieve message from receiver
    global receiver_name
    receiver_name = receiver.recv(1024).decode('utf-8')
    
    # send the e, n to receiver
    send_msg = str(e) + ',' + str(n)
    receiver.send(send_msg.encode('utf-8'))
    
    # recieve the public key from receiver
    global receiver_e, receiver_n
    receiver_e, receiver_n = receiver.recv(1024).decode('utf-8').split(',')
    receiver_e = int(receiver_e)
    receiver_n = int(receiver_n)
    
    # start chat by starting two threads for sending and receiving messages
    send_msg_thread = Thread(target=send_message, args=(receiver,))
    receive_message_thread = Thread(target=receive_message, args=(receiver,))
    send_msg_thread.start()
    receive_message_thread.start()
    send_msg_thread.join()
    receive_message_thread.join()
    
    
# send message to receiver
def send_message(receiver):
    while True:
        send_msg = input().lower()
        encrypted_msg = encrypt(send_msg, receiver_e, receiver_n)
        for block in encrypted_msg:
            # send the block to sender
            block = str(block)
            receiver.send(block.encode('utf-8'))
            # sleep for 0.002 seconds
            time.sleep(0.002)
        # send the end of message to sender
        receiver.send('\n'.encode('utf-8'))


# recieve message from receiver
def receive_message(receiver):
    recv_msg = ''
    while True:
        # concat the message with the previous message
        _end = receiver.recv(1024).decode('utf-8')
        if _end == '\n':
            print (receiver_name, ": ", recv_msg, flush=True)  
            recv_msg = ''
        else:
            recv_msg += decrypt(int(_end), d, n)
        

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
    
    sender.listen(1)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    sender.close()
