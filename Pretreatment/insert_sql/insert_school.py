from Pretreatment.insert_sql import utils


def insert_school():
    conn, c = utils.connect_sql()
    school_data = utils.read_csv(path='../result/school.csv')
    for row in school_data.itertuples():
        school_id = row[2]
        name = row[3]
        level_name = row[12]
        type_name = row[14]
        belong = row[16]
        f985 = row[35]
        f211 = row[15]
        province = row[33]
        city = row[23]
        county = row[30]
        nature_name = row[32]
        dual_class_name = row[37]
        hot = row[38]
        logo = row[40]
        num_subject = row[41]
        num_master = row[42]
        num_doctor = row[43]
        short = row[44]
        rank = row[7]
        email = row[45]
        address = row[46]
        phone = row[47]
        site = row[48]
        create_date = row[49]
        area = row[50]
        sql = f"INSERT INTO School (school_id,name,level_name,type_name,belong,f985,f211,province_id," \
              f"city,county,nature_name,dual_class_name,hot,logo,num_subject,num_master,num_doctor," \
              f"short,rank,email,address,phone,site,create_date,area) VALUES ('{school_id}','{name}'," \
              f"'{level_name}','{type_name}','{belong}','{f985}','{f211}','{province}','{city}','{county}'," \
              f"'{nature_name}','{dual_class_name}','{hot}','{logo}','{num_subject}','{num_master}','{num_doctor}'," \
              f"'{short}','{rank}','{email}','{address}','{phone}','{site}','{create_date}','{area}')"
        print(sql)
        c.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    insert_school()
