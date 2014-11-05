import pyaudio
import wave
import numpy as np
import pylab 
import array
import scipy.signal
from struct import *
import pylab     as pl

def pc_audio_downgrade(audiodata, by, size):
    outputstream = []
    index = 0
    sindex = 0
    abortat = int(len(audiodata) / size) * size
    # loop thru all items in the audio data
    for data in audiodata:
        # if the data chunk index is == to our down sample rate then
        if index >= by:
            # append the chunk to our down sample array
            outputstream.append(data)
        
        # move our sample counter up
        sindex = sindex + 1
        
        # see if we have passed our chunk counter
        if sindex >= size:
            # see if our index is at by
            if index == by:
                # if so reset
                index = 0
            else:
                index = index + 1
            sindex = 0
        abortat = abortat - 1
        if abortat <= 0:
            break
    return "".join(outputstream)


pylab.ion()
 
chunk = 1024
downsample = 10


wf = wave.open("echo_1.wav", 'rb')
p = pyaudio.PyAudio()

# open stream
stream = p.open(format=
                p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=8000,
                output=True)
# read data
#data = wf.readframes(chunk)
#adata = array.array('i', data)


data_sample_rate = wf.getframerate()
print "Sound Rate is at", data_sample_rate

# Define some info about or FIR Filter
FIR_TAPS = 13
FIR_Freq_MASK = np.array([0, 10, 50, 8010 / 2])
FIR_gain_MASK = np.array([3, 0])
FIR_weight_MASK = np.array([1, 1])
#print FIR_COFF
#exit()
FIR_COFF = scipy.signal.firwin(FIR_TAPS, cutoff=3000, window="hamming",nyq=104000/2)
#FIR_COFF = scipy.signal.firwin(FIR_TAPS,  50, pass_zero=False,nyq=20400/2)
#FIR_COFF = scipy.signal.firwin(FIR_TAPS, [0.05, 0.35], pass_zero=False)
print FIR_COFF

data = wf.readframes(chunk)

while data != '':
    cast_output = array.array('h', data)
    Fir_output = []
    
    for lx in range(len(cast_output) - 1, -1, -1):
        FIR_data = 0
        for lp in range(0, FIR_TAPS):
            if lx - lp < 0:
                FIR_data = FIR_data + FIR_COFF[lp] * 0
            else:
                FIR_data = FIR_data + FIR_COFF[lp] * cast_output[lx - lp]
                #FIR_data=cast_output[lx] 
            #print FIR_COFF[lp], cast_output[lp]
          
        Fir_cast = FIR_data.astype(np.int16)
        Fir_output.insert(0, pack('h', Fir_cast)) 
    
    #Fir_cast.tostring()
    #stream.write("".join(cast_output))
    cast_output.tostring()
    stream.write("".join(Fir_output))
    #stream.write(Fir_cast)
    data = wf.readframes(chunk)

stream.close()
p.terminate()