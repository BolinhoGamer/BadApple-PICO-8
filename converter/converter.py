import os
from _thread import start_new_thread as thread
from math import floor
from PIL import Image

if os.name == 'nt': os.system('')


# Thread ID
def process(tid: int):
    global completed_frames_count, active_thread_count
    
    idx = tid
    skip = round(30 / FPS)

    while idx * skip < num_frames:
        # Resizes the frame
        frame = Image.open(f'unprocessed_frames/{frames_name[floor(idx * skip)]}')
        w, h = frame.size
        
        factor = TARG_WIDTH / w
        w = floor(w * factor)
        h = floor(h * factor)
        
        frame = frame.resize((w, h))
        frame.convert('RGB')

        out = []
        # Process current frame
        for y in range(h):
            out.append(line := [])
            
            for x in range(w):
                pixel = frame.getpixel((x, y))[0] / 255
                line.append(1 if pixel > 0.5 else 0)
        

        converted_frames[floor(idx)] = out
        idx += 10
        completed_frames_count += skip

    active_thread_count -= 1


def convert():
    for i in range(num_frames):
        try: frame = converted_frames[i]
        except KeyError: continue

        tile_frames.append(converted_frame := [])
        
        for y, line in enumerate(frame):
            converted_frame.append(out := [])

            for x, pixel_tl in enumerate(line):
                tile = pixel
                if tile > 1: print(tile)

                out.append(tile)


def compress():
    print(len(tile_frames[0][0])*len(tile_frames[0]))
    
    for frame in tile_frames:
        compressed_frames.append(compressed_frame := [])

        counter = -1
        last_tile = None
        for line in frame:
            for tile in line:
                if (last_tile is not None and last_tile != tile) or counter == 255:
                    compressed_frame.append(counter)
                    compressed_frame.append(last_tile)
                    counter = 0

                else:
                    counter += 1

                last_tile = tile

        compressed_frame.append(counter)
        compressed_frame.append(tile)


# Constants #
NUM_THREADS = 10
TARG_WIDTH = 16
FPS = 4
# --------- #


frames_name = os.listdir('unprocessed_frames')
num_frames = len(frames_name)
completed_frames_count = 0
converted_frames = {}
tile_frames = []
compressed_frames = []


# Starts the threads
active_thread_count = NUM_THREADS
for i in range(NUM_THREADS):
    thread(process, (i,))


# Show percentage while waits for all threads to stop
while active_thread_count > 0:
    ratio = completed_frames_count / num_frames

    print(f'[{"#"*round(ratio*50)}{" "*round(50-ratio*50)}]  -  {ratio:.2%}  -  {int(completed_frames_count)}/{num_frames} ')
    print(u'\u001b[1A', end='')

print('\n\nConverting to tiles...')
converter()

print('Compressing...')
compress()

print('Skip:', round(30/FPS))

with open('frames.bin', 'wb') as file:
    for frame in compressed_frames:
        file.write(bytearray(frame))
