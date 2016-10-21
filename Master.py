import socket
import sys
import string
import struct
import binascii

# Create a TCP/IP socket
myRID = 0
myGID = 1
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#both IPaddress and nextSlaveIP are initially set to the master IP
IPaddress = socket.gethostbyname(socket.gethostname())
nextSlaveIP = IPaddress
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
    print 'Master: Waiting for a connection'
    connection, client_address = sock.accept()
    try:    # Receive the data in small chunks and retransmit it
        print 'Master: Received connection from', client_address
        
        client_IP = client_address[0] 
        client_Port = client_address[1]
        print 'Master: IP address of slave =', client_IP
        print 'Master: Port number of slave =', client_Port

        #IPaddress(master IP) is assigned to the newly received node IP
        nextSlaveIP = IPaddress
        IPaddress = client_IP

        data = connection.recv(16)
        dataCharArray = list(binascii.hexlify(data))
        #GIDReceived is the GID of the creator or the slave
        GIDReceived_String = str(dataCharArray[0]) + str(dataCharArray[1])
        #magicNumber is used by the nodes to test the validity of messages using this protocol
        #ignore the request if the message is not valid (different from 3 bytes or not containing the magic number).
        magicNumber_String = str(dataCharArray[4]) + str(dataCharArray[5]) + str(dataCharArray[2]) + str(dataCharArray[3])

        GIDReceived = int(GIDReceived_String)
        magicNumber = int(magicNumber_String)

        print 'Master: GIDReceived =', GIDReceived
        print 'Master: magicNumber =', magicNumber

        #print 'nextSlaveIP text to binary', binascii.hexlify(socket.inet_aton(nextSlaveIP))
        nextSlaveIPArray = bytearray.fromhex(binascii.hexlify(nextSlaveIP))
        tempArray = nextSlaveIP.split(".")
        print (tempArray[0])
        IP_part1 = bin(int(tempArray[0]))
        IP_part2 = bin(int(tempArray[1]))
        IP_part3 = bin(int(tempArray[2]))
        IP_part4 = bin(int(tempArray[3]))

        reply = struct.pack("=bhbBBBB", myGID, magicNumber, myRID, IP_part1, IP_part2, IP_part3, IP_part4)

        if reply:
            print 'Master: Sending data back to the client'
            connection.sendall(reply)
            print 'Master: Sent %s bytes back to %s' % (len(reply), client_IP)

        else: #no more data to read
          break       
         
 
            
    finally:
        # Clean up the connection
        connection.close()