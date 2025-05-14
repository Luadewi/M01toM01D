import struct
import sys
import os

if(len(sys.argv) <= 1):
    print("Pleace specify a file name")
    exit()

if not os.path.exists('user'):
    os.makedirs('user')

with open(sys.argv[1], 'rb') as f:
    source_data = bytearray(f.read())

metadata_file = bytearray(bytes.fromhex('20 01 00 00 4D 30 31 57 07 00 00 00 00 00 00 00 00 00 00 00 0A 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0A 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'))


for track_num in range (10):
    track_metadata_addr = 12 + 40 * track_num
    track_ptr_addr = track_metadata_addr + 24
    track_id = track_num + 0x100000

    if source_data[track_metadata_addr] == 1:
        (track_addr,) = struct.unpack('<I', source_data[track_ptr_addr : track_ptr_addr + 4])
        (track_region,) = struct.unpack('<I', source_data[track_ptr_addr + 4 : track_ptr_addr + 8])

        track_data = source_data[track_addr:track_addr + track_region]

        filename = "user/M01Dn_" + f"{track_id:0{8}x}"
        with open(filename, 'wb') as f:
            f.write(track_data)
        print("Extracted track " + str(track_num))
        
    metadata_file[0x4d + track_metadata_addr : 0x4d + track_metadata_addr + 40] = source_data[track_metadata_addr : track_metadata_addr + 40]
    metadata_file[0x41 + track_ptr_addr : 0x41 + track_ptr_addr + 4] = struct.pack('<I', track_id)

with open('user/M01Dn_00000000', 'wb') as f:
    f.write(metadata_file)
print("Created metadata file")
print("Save file converted successfully")