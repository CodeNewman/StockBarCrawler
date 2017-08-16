#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zhongliang.jiang
# @Date:   2017-08-16 14:57:39
# @Last Modified time: 2017-08-16 18:57:55
import requests
import fileinput
import time
import datetime
import os
import json


# local stock symbol config path
STOCK_SYMBOL_FILE = '../data/stock_code.txt'
# web address
WEB_URL = 'http://d.10jqka.com.cn/v2/line/hs_%s/%s/%s.js'  # symbol  00 No, 01 before, 02 later  year


class stock_bar_crawler(object):
    """
        stock bar information crawler
    """

    # stock year
    _year = 'last'
    # local file save path
    _save_flie_path = '../data/' + _year + '/'
    # flag stock code
    _stock_code = '600000'


    def __init__(self):
        pass


    def craw_stocks(self, stock_symbol_file_name, year = 'last'):
        """
            start crawling the data
        :arg year: stock year
        :arg stock_symbol_file_name
            stock symbol file
        """
        self._year = year

        if not os.path.exists(self._save_flie_path):
            os.makedirs(self._save_flie_path)


        for line in open(stock_symbol_file_name):
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

        url_00 = WEB_URL % (stock_id, '00', self._year)
        url_01 = WEB_URL % (stock_id, '01', self._year)

        # print(url_00)
        # print(url_01)

        r_00 = requests.get(url_00)
        r_01 = requests.get(url_01)

        if r_00.status_code == 200 and r_01.status_code == 200:
            index_00 = r_00.text.find("(");
            index_01 = r_00.text.find("(");

            if index_00 > 0 and index_01 > 0:
                web_data_00 = r_00.text[index_00 + 1:-1]
                web_data_01 = r_01.text[index_01 + 1:-1]

                web_data_json_00 = json.loads(web_data_00)
                web_data_json_01 = json.loads(web_data_01)

                # print('web_data_json_00  ' + web_data_json_00['data'])
                # print('web_data_json_01  ' + web_data_json_01['data'])

                self.save_to_file(stock_id, str(web_data_json_00['data']).split(';'),
                                  str(web_data_json_01['data']).split(';'))
            else:
                print('The vlid data location of th returned result is not found!')
        else:
            print('There is an exception to the page response!')


    def save_to_file(self, t_id, t_stock_data_00, t_stock_data_01):
        """
        Save th data sheet file.
        """
        length = len(t_stock_data_00)
        # print('t_stock_data_00  ' + str(t_stock_data_00))
        # print('t_stock_data_01  ' + str(t_stock_data_01))

        if len(t_stock_data_00) == len(t_stock_data_01) and length > 5:
            # print("length equality")
            contents = []
            for data_row_00, data_row_01 in zip(t_stock_data_00, t_stock_data_01):
                # print('data_row_00  ' + data_row_00)
                # print('data_row_01  ' + data_row_01)

                data_row_arr_00 = data_row_00.split(',')
                data_row_arr_01 = data_row_01.split(',')

                data_row = self.assembly_data(t_id, data_row_arr_00, data_row_arr_01)
                # print("单行数据  " + data_row)

                contents.append(data_row)

            contents = "\n".join(contents)

            file_name = self._save_flie_path + '%s.txt' % (t_id)
            file_object = open(file_name, 'w+')
            try:
                file_object.write(contents)
                file_object.flush()
            finally:
                """"""
                file_object.close()


        else:
            """
            Output exception message
            """
            print("An exception to the array length.")
            print(t_stock_data_00)
            print(t_stock_data_01)


    def assembly_data(self, t_id, t_data_row_arr_00, t_data_row_arr_01):
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
        # print(t_data_row_arr_00)
        # print(t_data_row_arr_01)

        space_mark = ','

        save_data_str = \
            str(t_id) + space_mark + \
            str(t_data_row_arr_01[0]) + space_mark + \
            str(t_data_row_arr_01[1]) + space_mark + \
            str(t_data_row_arr_01[2]) + space_mark + \
            str(t_data_row_arr_01[3]) + space_mark + \
            str(t_data_row_arr_01[4]) + space_mark + \
            str(t_data_row_arr_01[5]) + space_mark + \
            str(t_data_row_arr_00[1]) + space_mark + \
            str(t_data_row_arr_00[2]) + space_mark + \
            str(t_data_row_arr_00[3]) + space_mark + \
            str(t_data_row_arr_00[4]) + space_mark + \
            str(t_data_row_arr_00[5])
        return save_data_str

    # 提供一个查询的方式，给你一个symbol，快速的查询数据
    def query(self, t_stock_code, t_year='last', date = None):
        """
            query stock bar data
        :arg t_stock_code
            stock number , six bit. egg: 600000
        :arg year
            stock year egg: 2017
        :arg date
            stock date egg: xxxx-xx-xx 2017-01-01
        :return
            stock bar data, a data dictionary
        """
        self._year = t_year
        self._stock_code = t_stock_code

        stock_data = self.init_stock_data()
        if date is None:
            return stock_data
        else:
            return stock_data[str(date)]


    def init_stock_data(self):
        """
            open file and init stock data
        """
        stock_data = {}
        stock_data['stock_code'] = self._stock_code
        stock_symbol_file_name = self._save_flie_path + '%s.txt' % (str(self._stock_code))
        for line in open(stock_symbol_file_name):
            line = line.strip("\n")
            line = line.split(',')
            quary_data = self.assembly_quary_data(line)
            stock_data[str(line[1])] = quary_data

        return stock_data


    def assembly_quary_data(self, t_line):
        """"""
        result = {}
        result["dead_price"] = {
            "open": t_line[2],
            "high": t_line[3],
            "low": t_line[4],
            "close": t_line[5],
            "volume": t_line[6]
        }
        result["ex_right_price"] = {
            "open" : t_line[7],
            "high": t_line[8],
            "low": t_line[9],
            "close": t_line[10],
            "volume": t_line[11]
        }
        return result

def main():
    """
    main function
    :params:
        :name: xxxxx
    :return:
        xxxxx
    """

    crawler = stock_bar_crawler()
    crawler.craw_stocks(STOCK_SYMBOL_FILE, 'last')
    val = crawler.query('601688', 'last')
    print(val)
    val = crawler.query('601688', 'last', 20170118)
    print(val)

if __name__ == '__main__':
    main()
