#import time,readline,thread,sys
#from sys import stdin
#def noisy_thread():
#    while True:
#        time.sleep(2.0)
        #sys.stdout.write('\r'+' '*(len(readline.get_line_buffer())+2)+'\r')
        
        #print 'Interrupting text!'
#        sys.stdout.write('> ' + readline.get_line_buffer())
       
        #readline.clear_history()
      
        #x=readline.get_line_buffer()
       
        #readline.get_line_buffer()=none
        #print ("input :",x)
       
#thread.start_new_thread(noisy_thread, ())
#while True:
#    s = raw_input('> ')
import threading as th
from time import sleep


def main():
    t = Test()
    t.go()
    #try:

    join_threads(t.threads)
    #except KeyboardInterrupt:
    #    print "\nKeyboardInterrupt catched."
    #    print "Terminate main thread."
    #    print "If only daemonic threads are left, terminate whole program."


class Test(object):
    def __init__(self):
        self.running = True
        self.threads = []

    def foo(self):
        while(self.running):
            print ' '
            sleep(2)

    def get_user_input(self):
        while True:
        #while(self.running):
            x = raw_input("Enter 'e' for exit: ")
            print("input",x)
            if x.lower() == 'e':
               self.running = False
               break

    def go(self):
        t1 = th.Thread(target=self.foo)
        t2 = th.Thread(target=self.get_user_input)
        # Make threads daemonic, i.e. terminate them when main thread
        # terminates. From: http://stackoverflow.com/a/3788243/145400
        t1.daemon = True
        t2.daemon = True
        t1.start()
        t2.start()
        self.threads.append(t1)
        self.threads.append(t2)


def join_threads(threads):
    """
    Join threads in interruptable fashion.
    From http://stackoverflow.com/a/9790882/145400
    """
    for t in threads:
        while t.isAlive():
            t.join(5)


if __name__ == "__main__":
    main()