# -*- coding: utf-8 -*-
import MySQLdb
from textrank4zh import TextRank4Keyword, TextRank4Sentence

import sys
reload(sys)
sys.setdefaultencoding('utf8')

stopwords = ['支公司','公司','中国人寿','中国','人寿','国寿','财险','保险','股份','有限公司','中支','VIP',
             '俱乐部','电销中心','分公司','管理中心','订阅号','销售中心','财产','团队','营业部','顾问团',
             '个险','销售部','收展部','客服部']

#提取可能为地名的关键词
def extract_placename(place):
    word = TextRank4Keyword()
    word.analyze(place[0].encode('utf8', 'ignore'), window=2, lower=True)

    keywords = []
    for words in word.words_all_filters:
        for word in words:
            if word not in stopwords:
                keywords.append(word)

    print keywords

    return keywords

#判断可能的地名级别
def match_place(placename):
    match_city_sql = "select count(CityID) from s_city where CityName LIKE concat('" + placename + "','%')"
    match_district_sql = "select count(DistrictID) as count from s_district where DistrictName LIKE concat('" + placename + "','%')"
    match_provience_sql = "select count(ProvinceID) as count from s_province where ProvinceName LIKE concat('" + placename + "','%')"

    cursor2.execute(match_provience_sql)
    count = cursor2.fetchall()
    if count[0][0] > 0:
        return 1   #省级为1

    cursor2.execute(match_city_sql)
    count = cursor2.fetchall()
    if count[0][0] > 0:
        return 2   #市级为2

    cursor2.execute(match_district_sql)
    count = cursor2.fetchall()
    if count[0][0] > 0:
        return 3   #县区级为3

    first_name = ['李', '王', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴', '徐', '孙', '胡', '朱', '高', '林', '何', '郭',
                  '马', '罗', '梁', '宋', '郑', '谢', '韩', '唐', '冯', '于', '董', '萧', '程', '曹', '袁', '邓', '许', '傅',
                  '沈', '曾', '彭', '吕', '苏', '卢', '蒋', '蔡', '贾', '丁', '魏', '薛', '叶', '申', '余', '潘', '杜', '戴',
                  '夏', '钟', '汪', '田', '霍', '姜', '范', '方', '石', '姚', '谭', '廖', '邹', '熊', '金', '陆', '郝', '孔',
                  '白', '崔', '齐', '毛', '邱', '秦', '江', '史', '顾', '詹', '邵', '孟', '龙', '万', '岳', '辛', '钱', '汤',
                  '尹', '黎', '易', '常', '武', '乔', '贺', '葛', '龚', '文', '庞', '樊', '洪', '陶', '俞', '章', '鲁', '梅']

    if (placename[0] in first_name):
        return 4
    else:
        return 0

#更新级别到数据库
def update_level(wx_num, level):
    update_sql = "update wxnum set level='"+level+"' where wx_num='"+wx_num+"'"
    try:
        cursor.execute(update_sql)
        db.commit()
    except:
        print "update level where wx_num="+wx_num+" failed"

def run():
    select_sql = 'select wx_num_name,authentication,wx_num from wxnum'
    cursor.execute(select_sql)
    places = cursor.fetchall()

    for place in places:
        print place[0].encode('utf8', 'ignore') + " 的提取可能地名为 "
        level = 0
        for placename in extract_placename(place):
            if(match_place(placename)>level):
                level = match_place(placename)

        if level == 1:
            print "省级"
            update_level(place[2], '省级')
        elif level == 2:
            print "市级"
            update_level(place[2], '市级')
        elif level == 3:
            print "县区级"
            update_level(place[2], '县区级')
        elif level == 4:
            print "个人"
            update_level(place[2], '个人')
        print

# main
if __name__ == '__main__':
    print('connect to mysql server...')
    db = MySQLdb.connect(host='localhost', user='root', passwd='09181024', db='wechat', charset="utf8")
    db2 = MySQLdb.connect(host='localhost', user='root', passwd='09181024', db='places', charset="utf8")
    print('connect to mysql success!')
    cursor = db.cursor()
    cursor2 = db2.cursor()
    run()