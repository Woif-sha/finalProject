import snowboydecoder
import sys
import signal
import time

interrupted = False
#model = 'resources/models/snowboy.umdl'
model = 'Snowboy_xiaopie.pmdl'

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def callbacks():
    t = time.time()
    print(t)
    
def interrupt_callback():
    global interrupted
    return interrupted


if __name__ == "__main__":

#     if len(sys.argv) == 1:
#         print("Error: need to specify model name")
#         print("Usage: python demo.py your.model")
#         sys.exit(-1)
# 
#     model = sys.argv[1]
    print(model)
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.3)
    print('Listening... Press Ctrl+C to exit')

    # main loop
    detector.start(detected_callback=callbacks,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

    detector.terminate()
