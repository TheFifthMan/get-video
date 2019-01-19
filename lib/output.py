'''
@Description: 
@Version: 
@Author: 
@Date: 2019-01-12 15:16:52
@LastEditTime: 2019-01-18 22:47:58
'''
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style,init
init(autoreset=True)

def succeed_output(msg):
    print(Fore.GREEN + msg)
    
def failed_output(msg):
    print(Fore.RED + msg)

def parser(res):
    html = res.text
    soup = BeautifulSoup(html,'html.parser')
    return soup

 
if __name__ == "__main__":
    succeed_output("This is succeed message! ")
    failed_output("This is failed message! ")

    