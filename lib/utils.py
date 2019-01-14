'''
@Description: 
@Version: 
@Author: 
@Date: 2019-01-12 15:16:52
@LastEditTime: 2019-01-13 11:39:46
'''
import ctypes,os
from bs4 import BeautifulSoup

# 渲染
if os.name == 'nt':
    FOREGROUND_WHITE = 0x0007
    FOREGROUND_BLUE = 0x01 # text color contains blue.
    FOREGROUND_GREEN= 0x02 # text color contains green.
    FOREGROUND_RED  = 0x04 # text color contains red.
    FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN
    STD_OUTPUT_HANDLE= -11
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    def set_color(color, handle=std_out_handle):
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bool
    
else:
    FOREGROUND_WHITE = '\033[37m'
    FOREGROUND_GREEN= '\033[32m' # text color contains green.
    FOREGROUND_RED  = '\033[31m' # text color contains red.
    def set_color(color):
        return color


def succeed_output(msg):
    print(set_color(FOREGROUND_GREEN),msg,set_color(FOREGROUND_WHITE))
    
def failed_output(msg):
    print(set_color(FOREGROUND_RED),msg,set_color(FOREGROUND_WHITE))

def parser(res):
    html = res.text
    soup = BeautifulSoup(html,'html.parser')
    return soup

 
if __name__ == "__main__":
    succeed_output("This is succeed message! ")
    failed_output("This is failed message! ")

    