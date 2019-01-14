'''
@Description: 
@Version: 
@Author: 
@Date: 2019-01-12 15:15:28
@LastEditTime: 2019-01-12 21:13:56
'''
from lib.utils import succeed_output,failed_output
from engine.xiaohang import xhrun
import os

# 调试
import requests,re
from urllib.parse import quote
from bs4 import BeautifulSoup
import threading
from engine.dytt import dytt_run
    
def main():
    print(""" [-] 请根据以下序号进行选择：
    1. 搜索播放链接
    2. 搜索种子
    e. exit   
    """)

    choice = input(" [-] 请输入您的选择: ")
    if choice == "e":
        return 

    movies_name = input(' [-] 请输入视频名称： ')
    if choice == "1":
        xhrun(movies_name)
    elif choice == "2":
        ts = [
            threading.Thread(target=dytt_run,args=(movies_name,))
        ]
        for t in ts:
            t.start()
        for t in ts:
            t.join()
        with open('history/'+movies_name+".txt",'r',encoding='utf-8')as f:
            links = f.read()
        
        succeed_output("[√] 为您搜索到以下影片： \n{}".format(links))

    
    main()


if __name__ == "__main__":
    print("""
     ██████╗ ███████╗████████╗██╗   ██╗██╗██████╗ ███████╗ ██████╗ ███████╗
    ██╔════╝ ██╔════╝╚══██╔══╝██║   ██║██║██╔══██╗██╔════╝██╔═══██╗██╔════╝
    ██║  ███╗█████╗     ██║   ██║   ██║██║██║  ██║█████╗  ██║   ██║███████╗
    ██║   ██║██╔══╝     ██║   ╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║╚════██║
    ╚██████╔╝███████╗   ██║    ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝███████║
     ╚═════╝ ╚══════╝   ╚═╝     ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝         v1.0                                                                                                                 
    """)
    if not os.path.exists('history'):
        os.mkdir('history')
    main()

