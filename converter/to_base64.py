table = '"!@#$%&*()_=[]^~,.<>;:?|{}abcdefghijklmnopqrstuvwxyz0123456789+/'
#table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

last_str = ''
last_counter = 0

def to_base64(compressed_data):
    global last_str, last_counter
    
    out = ''

    buffer = ''
    for byte in compressed_data:
        buffer += bin(byte|0x100)[3:]

        while len(buffer) >= 6:
            seg = buffer[:6]
            buffer = buffer[6:]

            out += table[int(seg, 2)]

    while buffer:
        alignment = max(6 - len(buffer), 0)
        buffer += '0' * alignment
        #print(buffer, alignment)

        out += table[int(buffer, 2)] + '-' * alignment
        buffer = buffer[6:]

    if out == last_str:
        last_counter += 1
        return

    last_counter = 0
    last_str = out
    return out


def str_filter(frames):
    counter = -1
    for frame in frames:
        if frame is None:
            counter += 1

        else:
            if counter > -1:
                yield ' '*counter
                counter = -1

            yield frame

    if counter:
        yield ' '*counter


with open('frames.bin', 'rb') as file:
    compressed_data = file.read()


frames = [frame := []]
idx = 0
frame_size = 0

while idx < len(compressed_data):
    size = compressed_data[idx]
    tile = compressed_data[idx+1]
    idx += 2

    frame.append(size)
    frame.append(tile)

    frame_size += size + 1

    if frame_size == 192:
        frame_size = 0
        frames.append(frame := [])

frames.pop()


print(f'{len(frames)=}')
out = list(map((lambda x: f"'{x}'"), str_filter(map(to_base64, frames))))
print(f'{len(list(out))=}')

with open('b64.txt', 'w') as file:
    file.write('frame_data={\n')
    file.write(',\n'.join(out))
    file.write('\n}')
