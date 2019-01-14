# coding:utf-8
# https://www.btbtdy.tv
import requests,re
from urllib.parse import quote
requests.packages.urllib3.disable_warnings()
from lib.utils import parser, succeed_output, failed_output


root_url = "http://www.btbtdy.tv"
details_url = []

def search(movie_name):
    movie_name = quote(movie_name)
    url = root_url + "/search/"+movie_name+".html"
    r = requests.get(url,verify=False) 
    if r.status_code != 200:
        failed_output(r.text)
        return 
    try:
        soup = parser(r)
        links = soup.find_all('a',class_='so_pic')
        for url in links:
            url = re.sub("btdy/dy",'vidlist/',url['href'])
            details_url.append(root_url+url)
    except Exception as e:
        failed_output(e)


def parse_content():
    magnet = " -------从 btbtdy 搜索得到：-------\n"
    try:
        for url in details_url:
            r = requests.get(url)
            if r.status_code != 200:
                continue
            soup = parser(r)
            links = soup.find_all("a",class_="d1")
            titles = soup.find_all('a',class_='ico_1')

            for t,u in zip(titles,links):
                magnet += t['title']+":\n"+u['href']+"\n"
    except Exception as e:
        failed_output("[x] {}".format(e))
    return magnet

def btbtdy_run(movies_name):
    search(movies_name)
    magnet_links = parse_content()
    if details_url == []:
        failed_output("[x] 没有找到该内容。。。")
        return 
    with open('torrent/'+movies_name+".txt",'a')as f:
        f.write(magnet_links)
        



