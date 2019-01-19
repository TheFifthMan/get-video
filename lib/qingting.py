import os,sys
from lib.output import succeed_output,failed_output

def fm_run(p):
    banner = """ [-] 请输入你要听的电台编号：\t\n""" + " [{}].{} / ".format('e',"退出") + "[{}].{}\t\n".format('b',"返回")
    file = os.path.join(os.getcwd(),'lib','fm.txt')

    with open(file,'r',encoding="utf-8") as f:
        res = f.readlines()
    urls = []
    titles = [] 
    for i in range(1,len(res)+1):
        content = res[i-1].split("：")
        title = content[0]
        titles.append(title)
        urls.append(content[1].strip())
        if i % 3 == 0:
            banner += " [{}].{:<8s}\t\n".format(str(i-1),title)
            continue
        else:
            banner += " [{}].{:<8s}\t".format(str(i-1),title)
            
    print(banner) 
    
    ans = input(" [-] 请输入你的选择： ")
    if ans == "b" or ans == "b":
        p.stop()
        return
    if ans == 'e':
        p.stop()
        sys.exit(0)
    if ans:
        try:
            p.start_playing(urls[int(ans)])
            succeed_output(" [√] 正在播放: {}...".format(titles[int(ans)]))
        except:
            p.stop()
            failed_output(" [x] 无效选项")
    
    fm_run(p)