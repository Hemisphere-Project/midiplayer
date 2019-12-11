import subprocess, os, time, sys, signal
import mido

# Ctrl-c
def signal_handler(sig, frame):
        raise Exception('You pressed Ctrl+C! Goodbye :)')
signal.signal(signal.SIGINT, signal_handler)


# Start RTP virtual MIDI interface
basepath = os.path.dirname(os.path.realpath(__file__))
rtpmidid = subprocess.Popen( [os.path.join( basepath, 'bin/rtpmidid')] )
time.sleep(1)

# Mido
try:
    
    # Find rtpmidid interface
    midiout_name = None
    for iface in mido.get_output_names():
        if 'Network 128:0' in iface:
            midiout_name = iface
            break
    if not midiout_name:
        raise Exception('Error: no rtpmidid interface found', mido.get_output_names())

    # Open midi OUT
    midiout = mido.open_output(midiout_name)

    # Play it!
    for msg in mido.MidiFile('tetris.mid'):
        time.sleep(msg.time)
        print (msg)
        if not msg.is_meta:
            midiout.send(msg)
    
    time.sleep(10)

except Exception as e:
    print(str(e))



# Exit
rtpmidid.terminate()
exit(0)