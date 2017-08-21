# -*- encoding:utf-8 -*-

#----------------------------------
#
#  尝试使用nltk模块（朴素贝叶斯分类算法），使用articles表中的数据作为训练集，机器学习自主判断文章分类（正面、负面、中性）
#  此文件使用textrank4zh分词，由于负面样本太少，因此每个负面样本的特征计算两次
#  识别率一般，测试有效比例接近0.8，但测试集中有部分数据重复，所以最终效果有待测试
#
#----------------------------------

from textrank4zh import TextRank4Keyword, TextRank4Sentence
import MySQLdb
import nltk

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

print('connect to mysql server...')
db = MySQLdb.connect(host='localhost', user='root', passwd='09181024', db='wechat', charset="utf8")
print('connect to mysql success!')
cursor = db.cursor()

stopwords = ['人寿','人寿保险','中国','保险','公司','寿险','保险公司','上半年','股份','有限公司','今年','下半年','明日']
negwords = ['诈骗','黑幕','骗','骗取','拒赔','下跌','处罚','诱骗','亏损','恶意']

#处理单个title的线程
def gender_features(article_title):
    word = TextRank4Keyword()
    word.analyze(article_title, window=2, lower=True)

    #print '关键词:'
    keywords = []
    for words in word.words_all_filters:
        for word in words:
            if word not in stopwords:
                keywords.append(word)

    return keywords

def get_data_from_db():
    select_neg_article = "select article_title from articles where category='负'"
    select_pos_article = "select article_title from articles where category='正'"
    select_neu_article = "select article_title from articles where category='中'"

    cursor.execute(select_neg_article)
    negs = cursor.fetchall()
    neglist = [(neg[0],u'负') for neg in negs]

    cursor.execute(select_pos_article)
    poss = cursor.fetchall()
    poslist = [(pos[0], u'正') for pos in poss]

    cursor.execute(select_neu_article)
    neus = cursor.fetchall()
    neulist = [(neu[0], u'中') for neu in neus]

    return neglist+poslist+neulist

def decide_category(article_title):
    list = gender_features(article_title)
    num = 0
    for l in list:
        k = {}
        k["key"] = unicode(l)
        print k
        if (classifier.classify(k) == u"正"):
            print "正向 得分为1"
            num = num + 1
        elif (classifier.classify(k) == u"负"):
            print "负向 得分为-2"
            num = num - 2
        else:
            print "中向 得分为0"
            num = num


    print "总得分为"+str(num)

    if num > 1:
        #print "该标题的分类为：正向"
        return u"正"
    elif num < 0:
        #print "该标题的分类为：负向"
        return u"负"
    else:
        #print "该标题的分类为：中向"
        return u"中"

#负面样本太少，手动添加一些常见的负面特征
def append_neg_features(features):
    for neg in negwords:
        k = {}
        k["key"] = unicode(neg)
        list = (k, u"负")
        features.append(list)

    return features

#得到数据库中的数据
features = []
article_list = get_data_from_db()
for (n,g) in article_list:
    keywords = gender_features(n)
    for keyword in keywords:
        k = {}
        k["key"]=keyword
        list = (k,g)
        if (g == u"负"):
            features.append(list)
            features.append(list)
        else:
            features.append(list)

#features = append_neg_features(features)

print features
print len(features)

train,test = features,features #训练集和测试集
classifier = nltk.NaiveBayesClassifier.train(train) #生成分类器

print(nltk.classify.accuracy(classifier,test)) #测试准确度

classifier.show_most_informative_features(10)#得到似然比，检测对于哪些特征有用

#使用articles表中的数据进行训练和测试之后，尝试对article表中的文章进行分类
select_from_article_sql = "select article_title,article_id from article"
cursor.execute(select_from_article_sql)
articles = cursor.fetchall()
for article in articles:
    print article[0]
    category = decide_category(article[0]).encode('utf8', 'ignore')
    print article[0]+" 标题的分类为：" + category + "向\n"
    update_category_sql = "update article set category='"+category+"' where article_id="+str(article[1])
    try:
        cursor.execute(update_category_sql)
        db.commit()
    except:
        print "更新失败"

#while(True):
#    title=''
#    print '请输入要检测的文章标题:'
#    title = raw_input(title)
#    category = decide_category(title)
#    print "该标题的分类为："+category