import sys
import webrtcvad
import numpy as np
from mic_array import MicArray
import time
from pixels import Pixels
import threading

RATE = 16000
CHANNELS = 4
VAD_FRAMES = 10     # ms
DOA_FRAMES = 200    # ms

led_pos = 0
led_pos_changed = False
led_list = []

def get_result():
    global led_list
    while True:
        if(len(led_list) == 4):
            maxTimes = max(led_list,key=led_list.count)    # maxTimes指列表中出现次数最多的元素
            #print(maxTimes)
            #sys.stdout.write('\n')
            #sys.stdout.write('\n' + str(maxTimes) + '\n')
            if maxTimes <= 6:
                sys.stdout.write('Y ')
            else:
                sys.stdout.write('N ')
            led_list = []
        #threading.Event().wait(0.1)  # 0.1 0.05
    
def sound_indication_thread(pixel):
    global led_pos
    global led_pos_changed
    old_led_pos = None
    while True:
        if led_pos_changed:
            #sys.stdout.write('ssds')
            if old_led_pos!= led_pos:
                pixel.sound_indication(led_pos)
                old_led_pos = led_pos
            led_pos_changed = False
        # 可以添加适当的休眠时间，避免过度占用CPU资源
        #threading.Event().wait(0.1)

def main():
    global led_pos
    global led_pos_changed
    
    #pixel = Pixels()

    vad = webrtcvad.Vad(3)

    speech_count = 0
    chunks = []
    doa_chunks = int(DOA_FRAMES / VAD_FRAMES)
    time.sleep(0.5)
    
    try:
        with MicArray(RATE, CHANNELS, RATE * VAD_FRAMES / 1000)  as mic:
            #indicator_thread = threading.Thread(target=sound_indication_thread, args=(pixel,))
            #indicator_thread.start()
            
            result_thread = threading.Thread(target=get_result)
            result_thread.start()
            
            for chunk in mic.read_chunks():
                # Use single channel audio to detect voice activity
                if vad.is_speech(chunk[0::CHANNELS].tobytes(), RATE):
                    speech_count += 1
                    #sys.stdout.write('1')
                else:
                    pass
                    #sys.stdout.write('0')

                #sys.stdout.flush()

                chunks.append(chunk)
                if len(chunks) == doa_chunks:
                    if speech_count > (doa_chunks / 2):
                        frames = np.concatenate(chunks)
#                         print(len(frames))
#                         sys.exit()
                        direction = mic.get_direction(frames)
                        #pixel_ring.set_direction(direction) 
                        #print('\n{}'.format(int(direction)))
                        led_pos =  int((int(direction + 0.5) / (360 / 12)) + 0.5) % 12
                        led_list.append(led_pos)
                        #sys.stdout.write(str(led_pos) + ' ')
#                         if led_pos <= 6:
#                             #sys.stdout.write(str(led_pos) + '\n')
#                             #led_pos_changed = True
#                             sys.stdout.write('right\n')
#                         else:
#                             sys.stdout.write('left\n')
#sys.stdout.write(str(led_pos) + '\n')
#                         led_pos_changed = True
                        #print('led:{}'.format(led_pos))
                        #pixel.test()
                        #pixel.sound_indication(led_pos)
                        
                    speech_count = 0
                    chunks = []
                
                
                

    except KeyboardInterrupt:
        #pixel.off()
        pass
        
    #pixel_ring.off()
    #pixel.off()

if __name__ == '__main__':
    main()

