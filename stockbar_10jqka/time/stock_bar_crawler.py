#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zhongliang.jiang
# @Date:   2017-08-16 14:57:39
# @Last Modified time: 2017-08-17 13:58:49
import requests
import fileinput
import time
import datetime
import os
import json


# local stock symbol config path
STOCK_SYMBOL_FILE = './../../data/stock_code.txt'
# web address
# WEB_URL = 'http://d.10jqka.com.cn/v2/line/hs_%s/%s/%s.js'  # symbol  00 No, 01 before, 02 later  year
WEB_URL = 'http://d.10jqka.com.cn/v2/time/hs_%s/%s.js' # symbol  date '20170101' or 'last'

class stock_bar_crawler(object):
    """
        stock bar information crawler
    """
    # stock date
    _local_date = 'last'
    # local file save path
    _save_data_root_path = './../../data/time/'
    # flag stock code
    _stock_code = '600000'


    def __init__(self):
        pass

    def craw_stocks(self, stock_symbol_filename):
        """
            start crawling the data. Storage mode, the front of the right data (adj data).
        :arg date: stock date egg: '0930' ; 'last' as today
        :arg stock_symbol_filename
            stock symbol file
        """

        for line in open(stock_symbol_filename):
            line = line.strip("\n")
            line = line.split(':')
            id_str = str(line[1])
            print('climbing stock number : ' + id_str)
            self.craw(id_str)

        print('Crawl data completion!')

    def craw(self, stock_id):
        """
            crawl individual stock
        :type stock_id
            stock number
        """

        url_00 = WEB_URL % (stock_id,  self._local_date)
        r_00 = requests.get(url_00)

        if r_00.status_code == 200:
            index_00 = r_00.text.find("(")

            if index_00 > 0:
                web_data_00 = r_00.text[index_00 + 1:-1]

                web_data_json_00 = json.loads(web_data_00)['hs_' + stock_id]
                self._web_date = str(web_data_json_00['date'])
                web_date_time = web_data_json_00['data']
                if len(web_date_time) > 2:
                    self.save_to_file(stock_id, str(web_date_time).split(';'))
                else:
                    return
            else:
                print('The vlid data location of th returned result is not found!')
        else:
            print('There is an exception to the page response!')


    def save_to_file(self, t_stock_id, t_stock_data_00):
        """
        Save th data sheet file.
        """
        contents = []
        for data_row_00 in zip(t_stock_data_00):
            # print(type(data_row_00))
            # print('data_row_00', data_row_00)
            data_row_arr_00 = str(data_row_00[0]).split(',')
            # print('data_row_arr_00', data_row_arr_00)
            data_row = self.assembly_data(t_stock_id, data_row_arr_00)

            contents.append(data_row)

        contents = "\n".join(contents)

        file_path = self._save_data_root_path + self._web_date
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file_name = file_path + '/%s.txt' % (str(t_stock_id))
        file_object = open(file_name, 'w+')
        try:
            file_object.write(contents)
            file_object.flush()
        finally:
            """"""
            file_object.close()


    def assembly_data(self, t_stock_id, t_data_row_arr_00):
        """
        assembly row data
        :arg t_id
            stock number
        :arg t_data_row_arr_00
            data that no longer has power
        :arg t_data_row_arr_01
            the data of the previout powers
        :return:
            data
        """
        space_mark = ','
        save_data_str = \
            str(t_stock_id) + space_mark + \
            str(t_data_row_arr_00[0]) + space_mark + \
            str(t_data_row_arr_00[1]) + space_mark + \
            str(t_data_row_arr_00[2]) + space_mark + \
            str(t_data_row_arr_00[3]) + space_mark + \
            str(t_data_row_arr_00[4])

        return save_data_str

def main():
    """
    main function
    :params:
        :name: xxxxx
    :return:
        xxxxx
    """

    crawler = stock_bar_crawler()
    crawler.craw_stocks(STOCK_SYMBOL_FILE)


if __name__ == '__main__':
    main()