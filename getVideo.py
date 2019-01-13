'''
@Description: 
@Version: 
@Author: 
@Date: 2019-01-12 15:15:28
@LastEditTime: 2019-01-12 21:13:56
'''
from lib.output import succeed_output,failed_output
from lib.xiaohang import xhrun
import os

# 调试
import requests,re
from urllib.parse import quote
from bs4 import BeautifulSoup


    
def main():
    print(""" [-] 请根据以下序号进行选择：
    1. 搜索播放链接
    2. 搜索种子
    e. exit   
    """)

    choice = input(" [-] 请输入您的选择: ")
    if choice == "1":
        movies_name = input(' [-] 请输入视频名称： ')
        xhrun(movies_name)
    elif choice == "2":
        pass
    elif choice == 'e':
        return 
    
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

