from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urlencode

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings()


header={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'cookie':'',
    # 'origin':'https://www.douban.com',
    # 'Referer':'https://www.douban.com',
}

def get_page(i,base_url):
    '''
    获取指定豆瓣小组的第i页列表数据,返回网页源码
    base_url: 豆瓣小组列表的url，形如/group/{小组id}/discussion?，使用时根据实际情况替换。
    listcnt: 每页列表长度，影响每次分页的起点。默认为25。
    start: 分页起点。第1页起点为0。
    '''
    listcnt = 25
    start = listcnt*i
    params = {
        'start':start,
        'type':'new'
    }
    try:
        response = requests.get(base_url,headers=header,params=params,verify=False)
        # 因为verify=False，忽略对SSL证书的验证，可能会报Warning。不影响使用。
        print(response)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError:
        print('Error in ',base_url+urlencode(params))
        return None
    

def get_discussion_list(base_url):
    '''
    获取豆瓣指定小组的所有讨论贴列表数据，返回DataFrame。
    DataFrame各字段定义见 数据说明-按页爬取粉红税小组所有讨论的基本信息。
    base_url: 豆瓣小组列表的url，形如/group/{小组id}/discussion?，使用时根据实际情况替换。
    '''
    df = pd.DataFrame(columns=['title','elite','url','author-name','author-url','r-count','time','page','rank','timestamp'])

    for i in range(0,68):
        print('page:',i+1)
        res = get_page(i,base_url)
        # print(res)
        soup = BeautifulSoup(res, 'lxml')
        attrs = {'class':'olt'}
        raw_tb = soup.find(attrs=attrs).find_all('tr')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for rk,tr in enumerate(raw_tb[1:]):
            col = {}
            tds = tr.find_all('td')
            col['title'] = tds[0].find('a').get('title')
            if tds[0].find(attrs = {'class':'elite_topic_lable'}) !=None:
                col['elite'] = 1
            else:
                col['elite'] = 0
                
            col['url'] = tds[0].find('a').get('href')
            col['author-name'] = tds[1].find('a').get_text()
            col['author-url'] = tds[1].find('a').get('href')
            col['r-count'] = tds[2].get_text()
            col['time'] = tds[3].get_text()
            col['page'] = i+1
            col['rank'] = rk+1
            col['timestamp'] = timestamp
            # print(col)
            # print('==============================')
            df = df.append(col,ignore_index=True)
        sleep(3)
    return df
        
        
if __name__ == '__main__':
    grouplist_url = 'https://www.douban.com/group/711982/discussion?'
    # 根据实际小组链接进行替换
    list_df = get_discussion_list(grouplist_url)
    # 网页请求返回的列表可能会有重复部分，注意去重
    list_df.drop_duplicates(subset=['title','url'],inplace=True)
    list_df.to_csv('douban\data\discussion_list.csv',index=False,encoding='utf-8-sig')
    # 注意替换实际使用时的文件保存路径
    
    
    