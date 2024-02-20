import struct
from io import BytesIO
import vdf  # Updated import
import binascii
import json

class SubtitleSourceFormat:
    def __init__(self, lang):
        self.lang = lang

def compile(vdf_text_file_location:str):
    BLOCK_SIZE = 8192
    HEADER_SIZE = 24
    DIRECTORY_ENTRY_SIZE = 4 + 4 + 2 + 2  # crc + block index + offset + length

    vdf_text:str = None

    with open(vdf_text_file_location,"r") as fp:
        vdf_text = fp.read()
        fp.close()
    
    json_data:dict = json.loads(vdf_text)

    vdf_text = vdf.dumps(json_data)

    data = SubtitleSourceFormat(vdf.loads(vdf_text)["lang"])  # Updated usage
    buf = BytesIO()
    data_buf = BytesIO()

    # we divide data into `numblocks` blocks of `blocksize` size each
    # when the next string doesn't fit into the current block,
    # finalize the current one, write to the main buffer, and begin writing a

    block = BytesIO()

    entries = sorted(data.lang["Tokens"].items(), key=lambda x: x[0].lower())

    # header
    buf.write(b'VCCD')  # magic

    # version
    buf.write(struct.pack('<i', 1))

    # numblocks
    num_blocks_pos = buf.tell()
    buf.write(struct.pack('<i', 0))  # write later

    # blocksize
    buf.write(struct.pack('<i', BLOCK_SIZE))

    # directorysize = number of entries in the directory (to get size in bytes multiply with directory entry size)
    buf.write(struct.pack('<i', len(entries)))

    DICT_PADDING = 512 - (HEADER_SIZE + len(entries) * DIRECTORY_ENTRY_SIZE) % 512

    # dataoffset = where raw data starts (after header and all directory entries)
    buf.write(struct.pack('<i', HEADER_SIZE + len(entries) * DIRECTORY_ENTRY_SIZE + DICT_PADDING))

    directory_offset = buf.tell()  # directory entries begin here
    data_offset = buf.tell() + len(entries) * DIRECTORY_ENTRY_SIZE + DICT_PADDING  # raw data begins here

    if directory_offset != HEADER_SIZE:
        raise ValueError("Invalid header size")

    block_num = 0
    for token, string in entries:
        string_length = len(string) * 2 + 2  # utf16 + null terminator
        if len(block.getvalue()) + string_length >= BLOCK_SIZE:
            # new block time
            # write old block
            block_data_size = len(block.getvalue())
            padding_length = BLOCK_SIZE - block_data_size
            block.write(bytes(padding_length))  # pad with zeroes up to BLOCK_SIZE
            # append to data buffer
            old_offset = data_buf.tell()
            data_buf.write(block.getvalue())
            if data_buf.tell() != old_offset + BLOCK_SIZE:
                raise ValueError("Invalid size when appending current block to data")
            # create a new block
            block = BytesIO()
            block_num += 1

        # add to buffer
        old_offset = block.tell()
        block.write(string.encode('utf-16le'))
        block.write(struct.pack('<h', 0))  # null terminator
        written = block.tell() - old_offset
        if written != string_length:
            raise ValueError("Written string length is different from the string length predicted earlier on...")
        # add new dictionary entry
        crc = binascii.crc32(token.lower().encode()) & 0xFFFFFFFF
        buf.write(struct.pack('<I', crc))
        buf.write(struct.pack('<I', block_num))
        buf.write(struct.pack('<H', old_offset))
        buf.write(struct.pack('<H', written))

    # append the last block to data
    if len(block.getvalue()) > 0:
        # pad with zeros up to BLOCK_SIZE
        block_data_size = len(block.getvalue())
        padding_length = BLOCK_SIZE - block_data_size
        block.write(bytes(padding_length))  # pad with zeroes up to BLOCK_SIZE
        # append to data buffer
        old_offset = data_buf.tell()
        data_buf.write(block.getvalue())
        if data_buf.tell() != old_offset + BLOCK_SIZE:
            raise ValueError("Invalid size when appending last block to data")

    buf.write(bytes(DICT_PADDING))  # dictionary padding

    if buf.tell() != data_offset:
        raise ValueError("Ended up with an invalid dictionary size")

    # append data buffer to the main file buffer
    buf.write(data_buf.getvalue())

    expected_size = HEADER_SIZE + DIRECTORY_ENTRY_SIZE * len(entries) + DICT_PADDING + BLOCK_SIZE * (block_num + 1)
    if buf.tell() != expected_size:
        raise ValueError("Final size differs from the expected size")

    buf.seek(num_blocks_pos)
    buf.write(struct.pack('<i', block_num + 1))

    return buf.getvalue()

