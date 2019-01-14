'''
@Description: 
@Version: 
@Author: 
@Date: 2019-01-12 22:47:35
@LastEditTime: 2019-01-13 11:39:44
'''
import requests
requests.packages.urllib3.disable_warnings()
from urllib.parse import quote
from lib.utils import failed_output,succeed_output,parser
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
    
    soup = parser(r)
    urls = soup.find_all('a',class_="fl title")
    for url in urls:
        details_url.append(url['href'])


def parse_content():
    magnet_links = ""    
    for url in details_url:
        r = requests.get(root_url+url,verify=False)
        if r.status_code == 200:
            soup = parser(r)
            links = soup.find_all('a','fl btn-downLoad')
            for link in links:
                magnet_links += link['href'] + '\n'
    
    return magnet_links
    
def dytt_run(movies_name):
    search(movies_name)
    magnet_links = parse_content()
    with open('history/'+movies_name+".txt",'a')as f:
        f.write(magnet_links)
        




    