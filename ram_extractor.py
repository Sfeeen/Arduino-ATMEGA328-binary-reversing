
filename = "Blink_example_sfeeen.ino.BIN"
ram_out_filename = "INITIALISED_RAM"
reset_signature = b'\x11\x24\x1F\xBE\xCF\xEF\xD8\xE0'
ldi_r17_offset = 12

RAM_SIZE_BYTES = 2048

def find_signature_index_in_bytearray(signature, data):
    findex = 0
    remaining_data = data
    while(len(signature) < len(remaining_data)):
        remaining_data = data[findex:]
        # print(remaining_data)

        matches = True
        for index, byte in enumerate(signature):
            if remaining_data[index] != byte:
                matches = False

        if matches:
            return findex
        findex += 1

    return -1

def extract_ldi_argument(uint16_data):
    if(uint16_data & 0xF000 != 0xE000):
        print("Not an LDI instruction!!", end="")
        print(hex(uint16_data))

    low_byte = (uint16_data & 0xF)
    high_byte = (uint16_data & 0xF00) >> 4
    address = high_byte | low_byte
    # print(hex(address))
    return address

def get_combined_address(uint16_data_high, uint16_low):
    # print(hex(uint16_data_high))
    low_byte = extract_ldi_argument(uint16_low)
    high_byte = extract_ldi_argument(uint16_data_high)
    address = (high_byte << 8) | low_byte
    return address



def export_RAM_segment(filename):
    # Open the file in binary mode
    with open(filename, 'rb') as file:
        byte_array = bytearray(file.read())

    index = find_signature_index_in_bytearray(reset_signature, byte_array)
    if index < 0:
        print("Extraction failed! didn't find reset signature...")

    offset_byte_array = byte_array[index + ldi_r17_offset:]


    uint16_array = []

    for i in range(0, len(offset_byte_array), 2):
        total_uint16 = (offset_byte_array[i + 1] << 8) | offset_byte_array[i]
        uint16_array.append(total_uint16)

    dest_address = get_combined_address(uint16_array[2], uint16_array[1])
    print(f"Destination address: {hex(dest_address)}")

    source_address = get_combined_address(uint16_array[4], uint16_array[3])
    print(f"Source address: {hex(source_address)}")

    end_address = get_combined_address(uint16_array[0], uint16_array[8])
    print(f"end_address: {hex(end_address)}")

    # create RAM

    rambytearray = [0x00] * RAM_SIZE_BYTES

    while(dest_address != end_address):
        # print(hex(dest_address), hex(end_address))
        val = byte_array[source_address]
        rambytearray[dest_address] = val
        dest_address += 1
        source_address += 1

    # for i, b in enumerate(rambytearray):
    #     print(hex(i), hex(b))

    with open(ram_out_filename, "wb") as binary_file:
        for b in rambytearray:
            # print(hex(b))
            binary_file.write(b.to_bytes(1, byteorder='big'))

    print("done!")











if __name__ == '__main__':
    export_RAM_segment(filename)