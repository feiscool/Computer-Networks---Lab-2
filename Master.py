import socket
import sys
import struct
import binascii

		#when a node wants to join, 
		#assign it a ring ID myRID 
		#and the IP address of their successor node (nextSlaveIP)


# Create a TCP/IP socket
myRID = 0
myGID = 10015
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#get port number from argv
portNum = int(sys.argv[1])
# Bind the socket to the port
server_address = ('', portNum)
print('Master: Starting up on port #%d' % server_address)
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('Master: Waiting for a connection')
    connection, client_address = sock.accept()
    try:	# Receive the data in small chunks and retransmit it
    	print('Master: Received connection from %d' % client_address)
    	data = connection.recv(16)
    	dataCharArray = list(binascii.hexlify(data))
    	#GIDReceived is the GID of the creator or the slave
    	GIDReceived = str(dataCharArray[0]) + str(dataCharArray[1])
    	#magicNumber is used by the nodes to test the validity of messages using this protocol
    	#ignore the request if the message is not valid (different from 3 bytes or not containing the magic number).
    	magicNumber = str(dataCharArray[2]) + str(dataCharArray[3]) + str(dataCharArray[4]) + str(dataCharArray[5])

    	print('Master: GIDReceived = %d' % GIDReceived)
    	print('Master: magicNumber = %d' % magicNumber)
    
    	#reply = struct.pack("=bhbI", myGID, magicNumber, myRID, nextSlaveIP
    	# if reply:
    	# 	print('Master: Sending data back to the client')
    	# 	connection.sendall(reply)
    	# else: #no more data to read
    	# 	break		
         
 
            
    finally:
        # Clean up the connection
        connection.close()
