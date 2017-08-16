#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zhongliang.jiang
# @Date:   2017-08-16 09:16:08
# @Last Modified time: 2017-08-16 13:34:37
import requests
import fileinput
import time
import datetime
import os
import json

# 本地数据存放位置
FILE_PATH = 'data/k_line/' + str(datetime.date.today().isoformat()) + '/'

# 网络位置
WEB_URL = 'http://d.10jqka.com.cn/v2/line/hs_%s/%s/%s.js'  #symbol  00不,01前,02后  year

# 遍历文件并直接分析
def open_file(file_name):
    for line in fileinput.input(file_name):
        print(line.split(':')[1])
        craw(line.split(':')[1])

        time.sleep(100)
        
# 爬虫分析函数
def craw(t_id):
    id_str = str(t_id).replace('\n','')
    id_str = id_str.rjust(6, '0')

    url_00 = WEB_URL %(id_str, '00', '2017')
    url_01 = WEB_URL %(id_str, '01', '2017')

    print(url_00)
    print(url_01)

    r_00 = requests.get(url_00)
    r_01 = requests.get(url_01)

    if r_00.text.startswith('quotebridge_v2')  and r_01.text.startswith('quotebridge_v2') :
        web_data_00 = r_00.text[38:-1]
        web_data_01 = r_01.text[38:-1]

        web_data_json_00 = json.loads(web_data_00)
        web_data_json_01 = json.loads(web_data_01)

        save_to_file(id_str, str(web_data_json_00['data']).split(';'), str(web_data_json_01['data']).split(';'))

# 保存数据至文件
def save_to_file(t_id, t_data_00, t_data_01):
    length = len(t_data_00)

    if len(t_data_00) == len(t_data_01):
        file_name = FILE_PATH + '%s.txt' % (t_id)
        file_object = open(file_name, 'w+')

        i = 0
        while i < length:
            data_00 = t_data_00[i].split(',')
            data_01 = t_data_01[i].split(',')
            save_value(file_object, t_id, data_00, data_01)
            i += 1

        file_object.close()

# 把数据保存至文件流
def save_value(file, t_id, t_data_00, t_data_01):
    space_mark = ','

    save_data_str = \
        str(t_id) + space_mark +\
        str(t_data_01[0]) + space_mark +\
        str(t_data_01[1]) + space_mark +\
        str(t_data_01[2]) + space_mark +\
        str(t_data_01[3]) + space_mark +\
        str(t_data_01[4]) + space_mark +\
        str(t_data_01[5]) + space_mark + \
        str(t_data_00[1]) + space_mark +\
        str(t_data_00[2]) + space_mark +\
        str(t_data_00[3]) + space_mark +\
        str(t_data_00[4]) + space_mark +\
        str(t_data_00[5]) + '\n'

    file.write(save_data_str)
    file.flush()
    print(save_data_str)

# 检查并创建目录
def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print (path+' 创建成功')
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+' 目录已存在')
        return False

# 起始位置
def main():
    mkdir(FILE_PATH)
    open_file('data/stock_code.txt')

if __name__ == '__main__':
    main()
