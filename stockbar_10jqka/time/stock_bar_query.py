#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zhongliang.jiang
# @Date:   2017-08-17 10:04:09
# @Last Modified time: 2017-08-17 10:31:52
import datetime

class stock_bar_query(object):
    """
        stock bar information query
    """
    # stock year
    _date = 'last'
    # local file save path
    _save_flie_path = './../../data/time/'
    # flag stock code
    _stock_code = '600000'

    def __init__(self):
        pass

    # 提供一个查询的方式，给你一个symbol，快速的查询数据
    def query(self, t_stock_code, t_date='last', time=None):
        """
            query stock bar data
        :arg t_stock_code
            stock number , six bit. egg: 600000
        :arg date
            stock date egg: 20170101
        :arg time
            stock date egg: 0931 as 09:31
        :return
            stock bar data, a data dictionary
        """
        self._stock_code = t_stock_code
        if t_date == 'last':
            self._date = datetime.date.today().isoformat().replace("-", "")
        else:
            self._date = t_date

        stock_data = self.init_stock_data()

        if time is None:
            return stock_data
        else:
            return stock_data[str(time)]

    def init_stock_data(self):
        """
            open file and init stock data
        """
        stock_data = {}
        stock_data['stock_code'] = self._stock_code
        stock_symbol_file_name = self._save_flie_path + self._date + "/" + '%s.txt' % (str(self._stock_code))
        for line in open(stock_symbol_file_name):
            line = line.strip("\n")
            line = line.split(',')
            quary_data = self.assembly_quary_data(line)
            stock_data[str(line[1])] = quary_data

        return stock_data

    def assembly_quary_data(self, t_line):
        """"""
        result = {}

        result["time"] = t_line[0]
        result["price"] = t_line[1]
        result["volume"] = t_line[2]

        return result


def main():
    """
    main function
    :params:
        :name: xxxxx
    :return:
        xxxxx
    """

    query = stock_bar_query()
    val = query.query('601688', 'last')  # 'last' as today
    print(val)
    val = query.query('601688', '20170817', '0931')
    print(val)

if __name__ == '__main__':
    main()