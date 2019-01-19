# coding: utf-8 
'''
@Description: 
@Version: 
@Author: 
@Date: 2019-01-18 22:46:11
@LastEditTime: 2019-01-19 20:43:58
'''
import requests
from urllib.parse import quote
from lib.output import failed_output,succeed_output
import os,threading
from queue import Queue
from datetime import datetime,timedelta

Q = Queue()

url = "http://music.sonimei.cn/"
def search_music(pages,music_name,type_of_search):
    for i in range(1,pages + 1):
        payload = "input=" + quote(music_name) + "&filter=name&type="+ type_of_search +"&page=" + str(i)
        Q.put(payload)

def worker(music_name,headers2):
    while not Q.empty():
        payload = Q.get()
        headers = {
            "X-Requested-With":"XMLHttpRequest",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"
        }
        r = requests.post(url,data=payload,headers=headers)
        content = r.json()
        if content['code'] == 404:
            failed_output(" [x] {}".format(content['error']))
        else:
            for data in content['data']:
                with open(os.path.join("music",music_name+".m3u8"),'a') as f:
                    f.write(data['title'] + " " + data["author"] + "\n" + data['url'] + "\n")
                
                res = requests.get(data['url'],headers=headers2)
                
                path = os.path.join('music',data['author'])
                if not os.path.exists(path):
                    os.makedirs(path)
                
                
                if res.status_code == 200:
                    succeed_output(" [-] title: {} - {}".format(data['title'],res.status_code))
                    with open(os.path.join(path,data['title'] + ".mp3"),'wb')as f:
                        f.write(res.content)
                else:
                    failed_output(" [-] title: {} - {}".format(data['title'],res.status_code))

    

def music_run():
    music_name = input(" [-] 输入要搜索的音乐：")
    pages = int(input(" [-] 搜索几页数据："))
    type_of_search = input(""" [-] 请输入什么类型的搜索: \n [1] QQ音乐 [2] 酷狗音乐 [3]网易音乐 [4] 酷我音乐\n [-] 输入: """)
    if type_of_search == '1':
        type_of_search = 'qq'
        headers2 = {
                    "Host": "dl.stream.qqmusic.qq.com",
                    "Connection": "keep-alive",
                    "Cache-Control": "max-age=0",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                    "DNT": "1",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6",
                    "Range": "bytes=524288-524288",
                    "If-Range": "Fri, 17 Jun 1990 08:22:06 GMT",
                }
    elif type_of_search == '2':
        type_of_search = 'kugou'
        headers2 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": "fs.open.kugou.com",
            "If-Range": "Sun, 08 Mar 2000 10:24:20 GMT",
            "Range": "bytes=524288-524288",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        }
    elif type_of_search == '3':
        type_of_search = 'netease'
    elif type_of_search == '4':
        type_of_search = 'kuwo'
        headers2 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": "other.web.nf01.sycdn.kuwo.cn",
            "If-Range": "5b5964e9-3c59f7",
            "Range": "bytes=337008-337008",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }

    search_music(pages,music_name,type_of_search)
    ts = [ threading.Thread(target=worker,args=(music_name,headers2)) for i in range(30)]
    for t in ts:
        t.start()

    for t in ts:
        t.join()
        
    succeed_output(" [-] Completed")
    
if __name__ == "__main__":
    music_run(0,'宝贝疯客','qq')
    