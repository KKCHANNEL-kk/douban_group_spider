from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
import get_group_discussion as groupSpider


header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'cookie': '',
    # 'origin':'https://www.douban.com',
    # 'Referer':'https://www.douban.com',
}


def get_topic_info(url_list):
    '''
    根据讨论贴url列表，获取讨论贴的基本信息，返回DataFrame。
    url_list: 讨论贴url列表。
    content_df: 讨论贴内容(每贴第一条)的DataFrame。
    comment_df: 讨论贴回复的评论内容的DataFrame。
    '''
    content_df = pd.DataFrame(
        columns=['url', 'user', 'user_url', 'content', 'time', 'react_num', 'collect_num', 'timestamp'])
    comment_df = pd.DataFrame(columns=[
        'url', 'comment_id', 'user', 'user_url', 'comment', 'time', 'reply_to', 'timestamp'])

    for url in url_list:
        try:
            response = requests.get(url, headers=header, verify=False)
            soup = BeautifulSoup(response.text, 'lxml')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("url:%s, Time:%s" % (url, timestamp))
            
            # 顶楼部分
            content_raw = soup.find('div', class_='topic-doc')
            if content_raw is None:
                print('url:%s, content_raw is None' % url)
                continue
            user = content_raw.select('h3 > .from > a')[0].get_text()
            user_url = content_raw.select('h3 > .from > a')[0]['href']
            time = content_raw.select('h3 > .create-time')[0].get_text()
            content = content_raw.find(
                'div', id='link-report').get_text().strip()
            react_num = soup.find(
                'div', class_='action-react').find('span', class_='react-num').get_text()
            collect_num = soup.find(
                'div', class_='action-collect').find('span', class_='react-num').get_text()
            content_col = {'url': url, 'user': user, 'user_url': user_url, 'content': content,
                           'time': time, 'react_num': react_num, 'collect_num': collect_num, 'timestamp': timestamp}
            # print(content_col)
            content_df = content_df.append(content_col, ignore_index=True)

            # 评论部分
            comment_raw = soup.find('ul', id='comments')
            if comment_raw is None:
                print('url:%s, comment_raw is None' % url)
                continue
            
            comment_list = comment_raw.find_all('li')
            if comment_list is None or len(comment_list) == 0:
                print('url:%s, comment_list is Empty' % url)
                continue
            
            page = 1

            # 获取翻页按钮
            while len(soup.select('.paginator > .next > a')) > 0:
                com_res = requests.get(
                    url, params={'start': page*100}, headers=header, verify=False)
                page = page+1
                soup = BeautifulSoup(com_res.text, 'lxml')
                comment_raw = soup.find('ul', id='comments')
                # 将下一页的评论列表追加进common_list
                comment_list = comment_list + comment_raw.find_all('li')
                sleep(2 )

            for com in comment_list:
                # print(com)
                comment_id = com.get('data-cid')
                user = com.select('.reply-doc > div > h4 > a ')[0].get_text()
                user_url = com.select('.reply-doc > div > h4 > a ')[0]['href']
                time = com.select(
                    '.reply-doc > div > h4 > .pubtime')[0].get_text()
                comment = com.find(
                    'p', class_='reply-content').get_text().strip()
                if com.find('div', class_='reply-quote-content') is None:
                    reply_to = ''
                else:
                    reply_to = com.find(
                        'div', class_='reply-quote-content').get('data-ref-cid')
                comment_col = {'url': url, 'comment_id': comment_id, 'user': user, 'user_url': user_url,
                               'time': time, 'comment': comment, 'reply_to': reply_to, 'timestamp': timestamp}
                # print(comment_col)
                comment_df = comment_df.append(comment_col, ignore_index=True)

            sleep(1)
        except requests.ConnectionError:
            print('Error in ', url)
            continue
        
    return content_df, comment_df

if __name__ == '__main__':
    '''
    调用get_discussion_list函数获取url_list，
    或读取已经保存到本地的文件。
    '''
    # list_df = groupSpider.get_discussion_list()
    # list_df.drop_duplicates(subset=['title', 'url'], inplace=True)
    # list_df.to_csv('douban\data\discussion_list.csv',
    #                index=False, encoding='utf-8-sig')
    list_df = pd.read_csv('douban\data\discussion_list.csv')
    url_list = list_df['url'].tolist()

    content_df, comment_df = get_topic_info(url_list)
    content_df.to_csv('douban/data/discussion_content.csv',
                      index=False, encoding='utf-8-sig')
    comment_df.to_csv('douban/data/discussion_reply.csv',
                    index=False, encoding='utf-8-sig')
