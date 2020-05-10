from Pretreatment.insert_sql.insert_school_line import insert_school_line
from Pretreatment.insert_sql.insert_school import insert_school
from Pretreatment.insert_sql.insert_province_line import insert_province_line
from Pretreatment.insert_sql.insert_province import insert_province
from Pretreatment.insert_sql.insert_special import insert_special
from Pretreatment.insert_sql.insert_province_batch2 import insert_province_batch2


if __name__ == '__main__':
    insert_province()
    insert_special()
    insert_school()
    insert_province_line()
    insert_school_line()
    insert_province_batch2()
