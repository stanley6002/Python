#
# Python standard modules
#
import math
import time
import threading as th
import numpy as np
import pylab 
import array
from struct import *
#
# PyAudio
#
import pyaudio   as pa
#
# Pylab 
#(Numpy, Scipy, Matplotlib)
#
import scipy.signal
import pylab     as pl
global Glbvolume
Glbvolume=1.0
# my major audio class

# remove this line

class CHyAudio:
    def __init__(self, Fs= 102000 , TinSec= 10):
        print('RyAudio use %s'%pa.get_portaudio_version_text())
        
        self.Fs= Fs
        self.spBufferSize=    2048
        self.fftWindowSize= self.spBufferSize

        self.aP= pa.PyAudio()
        self.iS= pa.Stream(PA_manager= self.aP, input= True, rate= self.Fs, channels= 1, format= pa.paInt16)
        self.oS= pa.Stream(PA_manager= self.aP, output= True, rate= self.Fs,channels= 1, format= pa.paInt16)
        self.iTh= None
        self.oTh= None
        self.vol= None
        self.volume=1.0
        self.loopback=True
        self.lowpass=True
        #self.sound=     None
        #self.soundTime= 0
        self.gettingSound= True
        self.playingSound= True
        
        self.t= 0
        self.b= None  # byte string
        self.x= None  # ndarray
        self.fft= None
        self.f0= 0#None
        self.en= 0#None
        self.fm= 0#None # frequency mean
        self.fv= 0#None # frequency var
        self.fs= 0#None # frequency std
        self.enP= 0#None # AllPass
        self.enPL= 0#None # LowPass
        self.enPH= 0#None # HighPass

        self.entropy= 0#None

        self.frameI=   0

        self.frameN= self.spBufferSize/4  #1024/4 = 256
        self.TinSec= TinSec #10 # sec
        self.frameN= self.Fs*self.TinSec/self.spBufferSize #self.spBufferSize/4  #1024/4 = 256
        self.frameN= int(self.frameN)

        self.specgram= pl.random([self.frameN, self.spBufferSize/2])

        self.xBuf= pl.random([self.frameN, self.spBufferSize])

    def getSound(self):

        print('self.gettingSound= ',self.gettingSound)
        if self.lowpass :
          FIR_COFF= FIR_COFF_HP
        #else :
        #  FIR_COFF= FIR_COFF_HP
        #global globalSound, globalSoundTime, globalGettingSound, iS

        spBufferSize=  self.spBufferSize
        fftWindowSize= self.fftWindowSize
        
        Fir_output = []
        t0= time.time()
        while (self.gettingSound is True):
            try:
               self.b= b= self.iS.read(spBufferSize) # 1024
            except IOError:
               pass
            x= pl.fromstring(b,'int16')
            x= x.astype('float32')
            
            if self.loopback :
              self.xBuf[self.frameI%self.frameN]= self.volume*x
              
            else :
               x *= scipy.signal.triang(len(x))
               self.xBuf[self.frameI%self.frameN]= x 
              #del Fir_output[:]
            ### this is loopback line in/ out function
            
            
            
            t= time.time()-t0 # sec

            self.t= t   
            self.x= x   
            
            self.frameI +=1
            
        print('self.gettingSound= ',self.gettingSound)
        self.iS.stop_stream()

    def playSound(self):
        

        self.playingSound= True

        i= self.frameI - self.frameN//200
    
        while (self.playingSound is True): 

          
            x= self.xBuf[i%self.frameN]

            x= x.astype('int16')

           
            b= x.tostring()

          
            self.oS.write(b)

            i= self.frameI - self.frameN//200
            pass

        print('self.playingSound= ',self.playingSound)
        self.oS.stop_stream()

    def setVolume(self):
        while True:
        #while(self.running):
            element = raw_input("Enter command: ")
           
            if element.lower() == '+':
              
              if self.volume <=1.0:
                 self.loopback = True
                 self.volume= self.volume+0.1
              else :
                self.volume=1.2
                self.loopback = True
            print("increase volume")  
            if element.lower() == '-': 
                
              if self.volume >=0.0:
                 self.loopback = True
                 self.volume= self.volume-0.1 

            #  except ValueError:
            #  print "Not a float"
            if element.lower() == 'hp':
              self.loopback = False
              self.lowpass=False
            if element.lower() == 'lp':   
              self.loopback = False
              self.lowpass=True
            else : 
                self.loopback = True
              #if x.lower() == 'e':
               #self.running = False
               #break

    def setVol(self):
        
        self.vol= th.Thread(target= self.setVolume)
        self.vol.start()
       
        pass

    def startGet(self):
        
        self.iTh= th.Thread(target= self.getSound)
        self.iTh.start()
       
        pass

    def startPlay(self):
       
        self.oTh= th.Thread(target= self.playSound)
        self.oTh.start()
        
        pass

    def start(self):
       
        print('CHyAudio will start Get and Play....')
        self.startGet()
        self.startPlay()
        self.setVol()
        print('CHyAudio is started ....')

    def stop(self):
      
        self.gettingSound = False
        self.playingSound = False

        print('CHyAudio.stop is waiting for iS and oS are both stopped ...')

        while not (self.iS.is_stopped() and self.oS.is_stopped() ):
              #print('wait for iS and oS are both stopped')
              pass

        self.iS.close()
        self.oS.close()
        self.aP.terminate()

        print('CHyAudio.stop has been completed.')

Audio_in= CHyAudio

def demo00():
    
    Audio= Audio_in()
    Audio.start()

    print('30 seconds play and run ')

    time.sleep(50)

    print('main thread wakeup')

    Audio.stop()



if __name__=='__main__':

   demo00()
   #demo01()
   #demo02()
   #demo03()

   pass
