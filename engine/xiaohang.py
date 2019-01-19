# coding:utf-8
'''
@Description: 
@Version: 
@Author: 
@Date: 2019-01-12 15:51:53
@LastEditTime: 2019-01-18 22:49:50
'''
import requests,re
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup
from urllib.parse import quote
from lib.output import succeed_output,failed_output

# 配置
url = 'https://movie.xhboke.com/index.php/vod/search.html'
root_url = 'https://movie.xhboke.com'

# 功能函数
def search(movies_name):
    '''
    @param {type} 电影名字
    @return: 
    '''
    movies_name = quote(movies_name, 'utf-8')
    payload = "wd="+movies_name+"&submit="
    print(" [-] 正在影院中进行搜索...")
    headers = {
        'content-type': "application/x-www-form-urlencoded",
    }
    r = requests.post(url,data=payload,headers=headers,verify=False)
    if r.status_code == 200:
        succeed_output("[✓] 请求成功")
        return r
    else:
        failed_output("[x] 请求失败")
        return None

# 得到播放器播放到链接
# 实际播放的页面
def get_video(link):
    '''
    @param {type}  详细播放页面链接
    @return: 影片名字，播放器链接
    '''
    r = requests.get(root_url+link,verify=False)
    if r.status_code == 200:
        html = r.text
        result = re.search("link_next.*\"url\"\:(.*?)\,",html)
        link = re.sub(r'\\','',result.group(1))
        title = re.search("vod_part=\'(.*?)\'\;",html).group(1)

    else:
        title = ""
        link = "Error. The res is {}".format(r.text)
    return title,link

# 得到播放列表
def get_playlist(link):
    '''
    @param {type} 
    @return: 
    '''
    r = requests.get(root_url+link,verify=False)
    html = r.text
    soup = BeautifulSoup(html,'html.parser')
    div = soup.find(id='playlist1')
    links = div.find_all('a')
    return links 
    
# 解析获取实际播放的内容和视频标题
def parse_content(r):
    html = r.text
    soup = BeautifulSoup(html,"html.parser")
    results = soup.find_all('a',class_="stui-vodlist__thumb lazyload")
    count = 0
    if len(results) == 0:
        failed_output("[x] 没有找到该视频")
        return None,None

    succeed_output("[-] 一共搜索到 {} 部视频，根据输入以下序号进行下载...".format(len(results)))
    for result in results:
        title = result['title']
        succeed_output("[✓] {} - {}".format(count,title))
        count += 1

    # 获取播放列表
    if len(results) == 1:
        choice = 0
    else:
        choice = input(" [-] 请输入您的选择： ")
        
    if choice == "b":
        return None,None

    link = results[int(choice)]['href']
    title = results[int(choice)]['title']
    content = ""
    links = get_playlist(link)
        
    for url in links:
        url = url['href']
        t,u = get_video(url)
        succeed_output('[✓] '+t+" "+u)
        m3u8_url = get_m3u8(u)
        content += t+"\n"+m3u8_url + '\n'
    
    return title,content
        
            
# 获取真实到 m3u8 播放流
def get_m3u8(url):
    url = re.sub("\"","",url)
    if not re.search('m3u8',url):
        r = requests.get(url,verify=False)
        res = re.search("var main = \"(.*?)\"",r.text)
        res.group(1)
        link = re.sub("share/.*",res.group(1),url)
    else:
        link = url

    return link 
   

def xhrun(movies_name):
    r = search(movies_name)
    if r == None:
        failed_output('[x] 返回首页,请稍后再试...')
    else:
        title,content = parse_content(r)
        
        if title is None or content is None:
            return 
       
        with open('history/{}.m3u8'.format(title),'w')as f :
            f.write(content)
