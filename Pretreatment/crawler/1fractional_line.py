"""获取每个省份的分数线"""
import requests
from pyquery import PyQuery as pq
import pandas as pd
import os


def get_html(url):
    """获取网页源代码"""
    r = requests.get(url)
    r.encoding = r.apparent_encoding  # 解码，不然出现乱码现象
    return r.text


def get_data(html):
    """获取网页中的信息"""
    data = []
    doc = pq(html)
    none_div_city = set()
    for item in doc('.fsshowli').items():  # 获取所有个省份的table
        city = item('.city').text()
        years = list(map(lambda x: x.text(), item('.year').items()))
        for i, table in enumerate(item('.tline div table').items()):    # 获取每个省份，不同年份的table
            year = years[i]  # 数据对应年份
            for j, each_row in enumerate(table('.tr-cont').items()):    # 遍历每行
                row_data = each_row.text().split()
                length = len(row_data)
                if i == 0 and j == 0 and length == 2:  # 找出最新一年取消了文理分科的城市
                    none_div_city.add(city)
                if length == 2:  # 取消文理分科的
                    if row_data[1] == '-' or j == 0 or row_data[1] == '点击查看':
                        continue
                    data.append([city, year, '综合', row_data[0], row_data[1]])
                elif length == 3:  # 文理分科的
                    if row_data[1] == '-' or row_data[2] == '-' or row_data[1] == '点击查看' or row_data[2] == '点击查看':
                        continue
                    data.append([city, year, '文科', row_data[0], row_data[1]])
                    data.append([city, year, '理科', row_data[0], row_data[2]])

    print(none_div_city, '已取消文理分科')
    return data


def save_data(data, save_path='../result'):
    df = pd.DataFrame(data, columns=['省份', '时间', '学科类别', '批次', '分数线'])
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    df.to_csv(save_path+'/province_line.csv')


def main():
    url = 'https://www.eol.cn/e_html/gk/fsx/index.shtml'  # 获取历年高考分数线的url
    html = get_html(url)
    data = get_data(html)
    save_data(data)


if __name__ == '__main__':
    main()
