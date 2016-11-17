import serial
ser = serial.Serial("/dev/ttyAMA0")
ser.baudrate = 115200


ser.write("$$$")

read = ser.read(4)
print(read)
if read[0:3] != "CMD":
    print("Could not enter command mode")

ser.write("SM,0")
read = ser.read(4)
if read[0:3] == "ERR":
    print("Error entering slave mode")

ser.close()
