import socket
import sys
import string
import struct
import binascii

# Create a TCP/IP socket
myRID = 0
myGID = 1
magicNumber = 0x1234 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

myIPaddress = socket.gethostbyname(socket.gethostname())

#get port number from argv
portNum = int(sys.argv[1])
# Bind the socket to the port
server_address = ('', portNum)
print 'Master: Starting up on port', sys.argv[1]
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    # print 'Master: Waiting for a connection'
    connection, client_address = sock.accept()
    try:    # Receive the data in small chunks and retransmit it
        print 'Master: Received connection from', client_address
        
        client_IP = client_address[0] 
        client_Port = client_address[1]
        print 'Master: IP address of slave =', client_IP
        print 'Master: Port number of slave =', client_Port

        #IPaddress(master IP) is assigned to the newly received node IP
        nextSlaveIP = myIPaddress

        data = connection.recv(16)
        dataCharArray = list(binascii.hexlify(data))
        #GIDReceived is the GID of the creator or the slave
        GIDReceived = str(dataCharArray[0]) + str(dataCharArray[1])
        #magicNumber is used by the nodes to test the validity of messages using this protocol
        #ignore the request if the message is not valid (different from 3 bytes or not containing the magic number).
        received_magicNumber = str(dataCharArray[2]) + str(dataCharArray[3]) + str(dataCharArray[4]) + str(dataCharArray[5]) 

	GIDReceived = int(GIDReceived)
	received_magicNumber = int(received_magicNumber, 16)	

	print 'Master: GIDReceived =', GIDReceived
        print 'Master: magicNumber = 0x%x' % received_magicNumber

	if received_magicNumber != magicNumber:
		print 'Master: Error - invalid magic number received from Slave'
		exit(1)  

	packed_clientIP = struct.unpack("I", socket.inet_aton(nextSlaveIP))[0] 

        reply = struct.pack("!BHBI", myGID, magicNumber, myRID, packed_clientIP)

        if reply:
            print 'Master: Sending data back to the client'
            connection.sendall(reply)
            print 'Master: Sent %s bytes back to %s' % (len(reply), client_IP)

        else: #no more data to read
          break       
         
 
            
    finally:
        # Clean up the connection
        connection.close()
