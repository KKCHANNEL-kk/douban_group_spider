抓取豆瓣小组讨论贴列表，并通过列表中各帖子链接获取帖子的详细内容（评论文本）。两部分数据都写入在网页html源码中，基本不涉及ajax请求。

需求不复杂，因此直接使用requests构造请求获得html源码后，使用BeautifulSoup解析出所需字段，保存为本地csv文件。



## 1.  使用前准备
    

开发测试环境：Python 3.9.7

依赖包：

-   time 用于设置延时
-   datetime 用于获取当前时间戳
-   BeautifulSoup html解析
-   requests 网络请求
-   pandas 数据格式化存取（可选）
-   urllib 请求参数编解码

## 2.  参数解释
    

1.  `get_group_discussion.py`：获取小组所有讨论的基本信息。

-   `get_page(i)`：获取指定豆瓣小组的第i页列表数据
    -   base_url: 豆瓣小组列表的url，形如`/group/{小组id}/discussion?`，使用时根据实际情况替换。
    -   listcnt: 每页列表长度，影响每次分页的起点。默认为25。
    -   start: 分页起点。第1页起点为0。
-   `get_discussion_list(base_url)`：获取豆瓣指定小组的所有讨论贴列表数据，返回DataFrame。
    -   DataFrame各字段定义见`数据说明-按页爬取粉红税小组所有讨论的基本信息`。
    -   base_url: 豆瓣小组列表的url，形如`/group/{小组id}/discussion?`，使用时根据实际情况替换。

2.  `get_topic_content.py`：获取每条讨论贴的详细内容。

-   `get_topic_info(url_list)`：根据讨论贴url列表，获取讨论贴的基本信息，返回DataFrame。
    -   DataFrame各字段定义见`数据说明-每条讨论的第一条（1楼）`和`数据说明每条讨论的所有回复内容`。
    -   url_list: 讨论贴url列表。
    -   content_df: 讨论贴内容(每贴第一条)的DataFrame。
    -   comment_df: 讨论贴回复的评论内容的DataFrame。

## 3.  使用方法
    

1.  获取小组讨论贴列表

![小组讨论贴列表](https://ziukq44b05.feishu.cn/space/api/box/stream/download/asynccode/?code=ZmYwNGUzYzM3N2IzN2JhZjk4YmU2NjNlZGI5MzNhNDRfRDhMT0k4TGVEekhMRXBrSGkxUTZkVVJqRWtkTldKdktfVG9rZW46Ym94Y25xQzVtMTZqU1dYTU1Gbk1ORUNqQkJkXzE2NTM3MjkxMDY6MTY1MzczMjcwNl9WNA)

调用`get_group_discussion.py`，注意修改实际小组链接和文件保存路径。

![](https://ziukq44b05.feishu.cn/space/api/box/stream/download/asynccode/?code=YzA4ODRlNDVjZmFmMWIzNjg1N2IyNWEwYzNmMGMzMWVfZ0Y3RVlMZmd3MzlvQ0RpWE5BYzZmRVlEQ1ZOTFZMN05fVG9rZW46Ym94Y25MdUE5VDdiVzVMN09kbDBWZzRBR2lkXzE2NTM3MjkxMDY6MTY1MzczMjcwNl9WNA)

2.  获取讨论贴详细内容

![讨论贴详细内容](https://ziukq44b05.feishu.cn/space/api/box/stream/download/asynccode/?code=MGIzYmZhYjY4MmZhZDVmNmZkYmY1ODZiODA5ZWM3YWNfVE1XaEhVTGxvS0RoWXQ5aWE1MnhtSVJCSmVRNDhKbkxfVG9rZW46Ym94Y25ySlI1WENRa3VRNmJQVnJYMm10Y2hnXzE2NTM3MjkxMDY6MTY1MzczMjcwNl9WNA)

调用`get_topic_content.py`。可以先调用`get_group_discussion.py`中的函数获取小组帖子的url列表，或者读取已经保存到本地的url列表。

![](https://ziukq44b05.feishu.cn/space/api/box/stream/download/asynccode/?code=MDljYzliNTE1ZjRmOGQwZGI2MzJmNzk3NTUzMTkyZmRfQWZBZlpHZjRmcG84S3RRQWQwVUF2ckw5Sm84ak1UcWpfVG9rZW46Ym94Y25oZGU0R0VyYTlKY3N1T3BUUmdsVlNnXzE2NTM3MjkxMDY6MTY1MzczMjcwNl9WNA)

## 4. 数据说明
    

#### 按页爬取小组所有讨论的基本信息

文件名：discusstion_list.csv

说明：获取豆瓣小组的讨论列表，每条讨论点击进入得到正文，在这里分开采集。

url形如`https://www.douban.com/group/{小组id}/discussion`

参数为start，即起始位置，每次返回约28条。计算每页不同的start，拼接url批量爬取获得全量数据。

字段解释

| 字段名      | 解释             | 示例                                          |
|-------------|------------------|-----------------------------------------------|
| title       | 讨论帖子的标题   | 关于今天组内一位管理与几位组员之间的纠纷说明  |
| elite       | 是否加精         | 1                                             |
| url         | 帖子url          | https://www.douban.com/group/topic/258155059/ |
| author-name | 作者名           | Miaaaaaaaa                                    |
| author-url  | 作者url          | https://www.douban.com/people/157497953/      |
| r-count     | 点赞数           | 10                                            |
| time        | 发布时间         | 2022/1/19 5:46                                |
| page        | 爬取时所在页数   | 1                                             |
| rank        | 爬取时所在排名   | 2                                             |
| timestamp   | 爬取时间的时间戳 | 2022/5/22 18:27                               |


#### 每条讨论的第一条（1楼）

文件名：discussion_content.csv

说明：获取每条讨论帖子的正文（即作者发布的第一楼）。为减少数据耦合，讨论贴第一条和其余回复贴分别保存为两个文件。

url形如`https://www.douban.com/group/topic/{讨论贴id}/`

字段解释

| 字段名      | 解释                 | 示例                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|-------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| url         | 该讨论贴的url        | https://www.douban.com/group/topic/249979294/                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| user        | 发表用户名           | Σαπφώκορίτσι                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| user_url    | 发表用户url          | https://www.douban.com/people/Gra1989/                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| content     | 正文（即帖子第一楼） | 【大家好，原组长已经跑路，并把组长转让给了第一个回她消息的我。…… |
| time        | 发布时间             | 2021/10/16 10:48                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| react_num   | 点赞数               | 86                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| collect_num | 收藏数               | 2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| timestamp   | 爬取时间的时间戳     | 2022/5/22 22:27                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

#### 每条讨论的所有回复内容

文件名：discussion_reply.csv

说明：获取每条讨论帖子下面的评论内容和评论之间的回复关系。

字段解释

| 字段名     | 解释                 | 示例                                                                                                        |
|------------|----------------------|-------------------------------------------------------------------------------------------------------------|
| url        | 该讨论贴的url        | https://www.douban.com/group/topic/249979294/                                                               |
| comment_id | 该评论的id           | 4355647386                                                                                                  |
| user       | 发表评论的用户       | Σαπφώκορίτσι                                                                                                |
| user_url   | 发表评论用户的url    | https://www.douban.com/people/Gra1989/                                                                      |
| comment    | 评论内容             | 好滴，也许可以把大家之前的投票帖作为申请自荐帖，超过50票即成为组长候选人。然后在这个帖汇总投票选举新组长？� |
| time       | 评论发表时间         | 2021/10/16 10:57                                                                                            |
| reply_to   | 评论回复对象的评论id | 4355637025                                                                                                  |
| timestamp  | 爬取时间的时间戳     | 2022/5/22 22:27                                                                                             |