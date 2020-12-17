import struct

for i in range(1,10,2):
    print(i)

channelid1 = struct.pack('!H', 1)
channelid2 = struct.pack('!H', 2)
fenmiaocnt =struct.pack('!B', 100)
length = struct.pack('!B', 100)

print(len(channelid1))
print(len(fenmiaocnt))
print(len(length))
print(len(channelid1+fenmiaocnt+length))