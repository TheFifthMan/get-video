'''
@Description: 
@Version: 
@Author: 
@Date: 2019-01-12 22:47:35
@LastEditTime: 2019-01-18 22:49:42
'''
import requests
requests.packages.urllib3.disable_warnings()
from urllib.parse import quote
from lib.output import failed_output,succeed_output,parser
import queue
import threading
root_url = "https://www.dytt.in"
details_url = []

def search(movies_name):
    movies_name = quote(movies_name)
    url = root_url + '/search?s=' + movies_name
    r = requests.get(url,verify=False)
    if r.status_code != 200:
        failed_output("[x] Error! The status code is {}".format(r.status_code))
    try:
        soup = parser(r)
        urls = soup.find_all('a',class_="fl title")
        for url in urls:
            details_url.append(url['href'])
    except Exception as e:
        failed_output("[x] {}".format(e))
        


def parse_content():
    magnet_links = " -----从dytt得到：--------\n"
    try:
        for url in details_url:
            r = requests.get(root_url+url,verify=False)
            if r.status_code == 200:
                soup = parser(r)
                links = soup.find_all('a','fl btn-downLoad')
                for link in links:
                    magnet_links += link['href'] + '\n'
    except:
        pass
        

    return magnet_links
    
def dytt_run(movies_name):
    search(movies_name)
    magnet_links = parse_content()
    if details_url == []:
        return 
    with open('torrent/'+movies_name+".txt",'a')as f:
        f.write(magnet_links)
        




    