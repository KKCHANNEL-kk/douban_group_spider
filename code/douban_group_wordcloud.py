import jieba.analyse
import pandas as pd

data = pd.read_csv('data/discussion_content.csv')

docs = data['content']

topK = 20
tags = jieba.analyse.extract_tags(docs, topK=topK,withWeight=True)