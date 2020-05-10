"""获取院校录取信息,需先运行get_html和school_message"""
from glob import glob
import pandas as pd
import json
import os


def get_path_list(base_path='../result/school_detail'):
    path_list = glob(os.path.join(base_path, '*'))
    return path_list


def main():
    path_list = get_path_list()
    data_df = pd.read_csv('../result/school.csv')
    data_df['logo'] = ''
    data_df['num_subject'] = ''
    data_df['num_master'] = ''
    data_df['num_doctor'] = ''
    data_df['short'] = ''
    data_df['rank'] = ''
    data_df['email'] = ''
    data_df['address'] = ''
    data_df['phone'] = ''
    data_df['site'] = ''
    data_df['create_date'] = ''
    data_df['area'] = ''
    for path in path_list:
        with open(path, 'r', encoding='utf-8') as f:
            data = eval(f.read())
            detail_data = data['data']
            school_id = detail_data['school_id']
            logo = f'https://static-data.eol.cn/upload/logo/{school_id}.jpg'
            num_subject = detail_data['num_subject']
            num_master = detail_data['num_master']
            num_doctor = detail_data['num_doctor']
            short = detail_data['short']
            rank = detail_data['ruanke_rank']
            email = detail_data['email']
            address = detail_data['address']
            phone = detail_data['phone']
            site = detail_data['site']
            create_date = detail_data['create_date']
            area = detail_data['area']
            index = data_df[data_df.school_id == int(school_id)].index.tolist()[0]
            data_df.loc[index, 'logo'] = logo
            data_df.loc[index, 'num_subject'] = num_subject
            data_df.loc[index, 'num_master'] = num_master
            data_df.loc[index, 'num_doctor'] = num_doctor
            data_df.loc[index, 'short'] = short
            data_df.loc[index, 'rank'] = rank
            data_df.loc[index, 'email'] = email
            data_df.loc[index, 'address'] = address
            data_df.loc[index, 'phone'] = phone
            data_df.loc[index, 'site'] = site
            data_df.loc[index, 'create_date'] = create_date
            data_df.loc[index, 'area'] = area

            pro_type_min = detail_data['pro_type_min']
            one_school_line = []
            for province_id, value in pro_type_min.items():
                for d in value:
                    year = d['year']
                    for types, score in d['type'].items():
                        one_school_line.append([province_id, year, types, score])
            df = pd.DataFrame(one_school_line, columns=['province_id', 'year', 'types', 'score'])
            df.to_csv(f'../result/school_line/{school_id}.csv')
    data_df.to_csv('../result/school.csv')


if __name__ == '__main__':
    main()
