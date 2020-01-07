import os, struct, sys

def get_byte(data, offset):
    return struct.unpack('<B', data[offset])[0]
def get_word(data, offset):
    return struct.unpack('<H', data[offset:offset+2])[0]
def get_dword(data, offset):
    return struct.unpack('<I', data[offset:offset+4])[0]


with open(sys.argv[1], 'rb') as f:
    data = f.read()
    if get_word(data, 0)  != 0:
        raise SystemExit('Invalid ico prefix')
    if get_word(data, 2)  != 1:
        raise SystemExit('Not a ICO file')
    
    nr_icons = get_word(data, 4)
    print('Nr icons = ', nr_icons)

    # current offset
    co = 6
    for i in range(nr_icons):
        width = get_byte(data, co)
        height = get_byte(data, co + 1)
        palette = get_byte(data, co + 2)
        panes = get_word(data, co + 4)
        bits_per_px = get_word(data, co + 6)
        data_size = get_dword(data, co + 8)
        data_start = get_dword(data, co + 12)
        print('Image %d' % i)
        print('-- %d x %d ' % (width, height))
        print('-- palette: %d' % palette)
        print('-- panes: %d' % panes)
        print('-- bit per pixel: %d' % bits_per_px)
        print('-- data_size: %d (%X)' % (data_size, data_size))
        print('-- data_start: %d (%X)' % (data_start, data_start))
        name = '%s_%d.ico' % (sys.argv[1], i)
        with open(name, 'wb') as g:
            g.write('\x00\x00\x01\x00\x01\x00')
            header = data[co:co+16]
            header = header[:12] + struct.pack('<I', 22) + header[16:]
            g.write(header)
            if data_start + data_size > len(data):
                print('-- [Warning] Invalid data size')
            g.write(data[data_start:data_start+data_size])
        co += 16
        
    
    
        
     