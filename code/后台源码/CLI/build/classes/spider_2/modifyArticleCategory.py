# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------------
#
#  管理员点击修改一条文章的状态
#  传回后台文章在数据库的id和修改之后的状态
#  将数据库表article作为存储数据的表，修改对应id的文章状态
#  将数据库表articles作为分类器的训练集，将修改之后的文章加入articles表中等待下一次训练
#
#-------------------------------------------------------------------------------------------------------

import sys, MySQLdb
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf8')

class modify_category():
    def __init__(self, article_id, category):
        self.article_id = article_id
        self.category = category

    #修改数据库表article
    def modify_article_table(self):
        addDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_sql = ("update article set category='%s',add_time='%s' where article_id=%d" % (self.category,addDate,self.article_id))
        try:
            cursor.execute(update_sql)
            db.commit()
            print "update category success..."
        except:
            print "update category failed..."

        self.add_train_set()

    # 将修改后的数据加入数据库表articles中作为训练集
    def add_train_set(self):
        addDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        select_sql = ("select article_title,article_url,article_abstract,article_time,article_gzh_name," \
                     "article_gzh_url,article_gzh_headimg,category from article where article_id=%d" % self.article_id)
        try:
            cursor.execute(select_sql)
            info = cursor.fetchall()
        except:
            print "select article info failed..."

        add_sql =("INSERT INTO articles(article_title,article_url,article_abstract,article_time,"
                  "article_gzh_name,article_gzh_url,article_gzh_headimg,add_time,category) "
                  "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        add_data = (info[0][0],info[0][1],info[0][2],info[0][3],info[0][4],info[0][5],info[0][6],addDate,info[0][7])

        try:
            cursor.execute(add_sql, add_data)
            db.commit()
            print "add into train set success..."
        except:
            print "add into train set failed..."

# main
if __name__ == '__main__':
    print('连接到mysql服务器...')
    db = MySQLdb.connect(host='localhost', user='root', passwd='09181024', db='wechat', charset="utf8")
    #db2 = MySQLdb.connect(host='localhost', user='root', passwd='09181024', db='places', charset="utf8")
    print('连接上了!')
    cursor = db.cursor()
    #cursor2 = db2.cursor()
    modify_category(1,'中').modify_article_table()