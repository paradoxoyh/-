#author: oyh
#date: 2017-03-12
#还需要增强程序鲁棒性
#coding=utf-8
import requests
import re
import xlwt
import time

def getrootweb(url,header):
    res=[]
    url_high='https://movie.douban.com/subject/'
    url_low='/'
    ree_index=re.compile('"url":"https:.{4}movie.douban.com.{2}subject.{2}(\d*).{2}","playable"')
    ree_forbiden='Response [403]'
    post_param={'type':'moive',
            'tag':'经典',
            'sort':'recommend',
            'page_limit':'20',
            'page_start':'20'}

    try:
        data=requests.get(url,data=post_param,headers=header,verify=True,timeout=10)
    except Exception:
        print('Timeout')
        return False
    if ree_forbiden!=data:
        index_num=re.findall(ree_index,data.text)
        for i in index_num:
            url=url_high+i+url_low
            try:
            	res_=getsubweb(url,header)
            	if type(res_)!=bool:
            	    res.append(res_)
            	else:
            		raise AttributeError
            except AttributeError:
            	pass
        return res
    else:
    	print('IP已被禁用')
    	return False



def getsubweb(url,header):
    ree_content=[0,0]
    ret=[]
    ree_forbiden='Response [403]'
    ree_content[0]='<input type="hidden" name="title" value="(.*).*\((\d{4})\)">'
    ree_content[1]='<input type="hidden" name="desc" value="导演 (.*) 主演 .* (\d\.\d)分\((\d*)评价\)">'
    time.sleep(0.1)

    try:
        data=requests.get(url,headers=header,verify=True,timeout=15)
        print('正在解析网页:',url,'数据...')
    except Exception:
    	print('Timeout')
    	return False
    if data!=ree_forbiden:
        for i in ree_content:
            m=re.search(i,data.text)
            ret+=list(m.groups())
        ret+=[url]
        print(ret,'\n')
        return ret
    else:
    	print('IP已被禁用')
    	return False



if __name__=='__main__':
    cache=[]
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Cookie':'ue="494048906@qq.com;__ads_session=EydvnP3H6gjkiXQD6QA=',
            'Connection':'keep-alive',
            'Accept':'*/*',
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Host':'movie.douban.com',
            'Referer':'https://movie.douban.com/',
            'X-Request-With':'XMLHttpRequest'}
    url_rootweb='https://movie.douban.com/j/search_subjects?type=movie&tag=经典&sort=recommend&page_limit=20&page_start='
    
    for i in range(25):
        Url_rootweb=url_rootweb+str(i*20)
        temp=getrootweb(Url_rootweb,header)
        if type(temp)!=bool:
        	cache+=temp
    print('一共扒取了',len(cache),'条内容')
    
    f=xlwt.Workbook()
    sheet1=f.add_sheet('sheet1',cell_overwrite_ok=True)
    cache.insert(0,['电影','年份','导演','评分','打分人数','链接'])
    for i in range(len(cache)):
        for j in range(len(cache[0])):
            sheet1.write(i,j,cache[i][j])
    f.save('Data_movie_3.xls')