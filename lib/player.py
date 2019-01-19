from subprocess import Popen,PIPE
from lib.output import failed_output,succeed_output
import signal
import os,sys
if os.name == "nt":
    mpg123 = os.path.join(os.getcwd(),'third','mpg123','mpg123.exe')
else:
    mpg123 = "mpg123"

class Player():
    def __init__(self):
        self.handler = None
    
    def start_playing(self,url):
        self.stop()
        self.handler = Popen([mpg123,url],stdout=PIPE,stderr=PIPE)

    def stop(self):
        if self.handler is not None:
            try:
                self.handler.terminate()
                os.kill(self.handler.pid,signal.SIGTERM)
                self.handler = None
            except OSError as e:
                pass