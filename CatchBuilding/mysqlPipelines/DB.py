import pymysql
from CatchBuilding import settings


class DB:
    def __init__(self):
        # 打开数据库连接
        db_host = settings.MYSQL_HOST
        db_user = settings.MYSQL_USER
        db_password = settings.MYSQL_PASSWORD
        db_database = settings.MYSQL_DATABASE
        self.table = db_table = settings.MYSQL_TABLE

        try:
            self.db = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_database, charset='utf8')
        except:
            print('连接数据库失败')

    def insert(self, args, sql_type=''):
        db = self.db
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        sql = 'SET NAMES utf8'

        cursor.execute(sql)
        # SQL 插入语句
        if sql_type == 'images':
            sql = "INSERT INTO " + self.table + '_pictures' + "(`building_id_md5`, `filename`, `created_at`, " \
                                                              "`updated_at`)" \
                                                              "VALUES (%(building_id_md5)s, %(filename)s," \
                                                              " %(created_at)s, %(updated_at)s)"
        elif sql_type == 'update':
            sql = "update  " + self.table + " set address = \"" + args['address'] + "\" where original_id = \"" \
                  + args['original_id'] + "\""
        else:
            sql = "INSERT INTO " + self.table + "(`original_id`,`building_id`, `building_name`, `province`, `city`," \
                                                " `county`, `address`, `longitude`, " \
                                                "`latitude`, `description`, `type`, `total_floor`, `standard_area`, " \
                                                "`covered_area`, `clear_height`, `floor_height`, `room_rate`, " \
                                                "`completion_time`, `developer`, `property_fee`, `elevators_number`," \
                                                " `parking_number`, `conditioning_type`, `security_system`," \
                                                " `property_company`, `public_transport`, `picture_urls`, `created_at`," \
                                                " `updated_at`) " \
                                                "VALUES (%(original_id)s, %(building_id)s, %(building_name)s," \
                                                " %(province)s, %(city)s, %(county)s, %(address)s, %(longitude)s," \
                                                " %(latitude)s, %(description)s, %(type)s, %(total_floor)s," \
                                                " %(standard_area)s, %(covered_area)s, %(clear_height)s," \
                                                " %(floor_height)s, %(room_rate)s, %(completion_time)s, %(developer)s," \
                                                " %(property_fee)s, %(elevators_number)s, %(parking_number)s," \
                                                " %(conditioning_type)s, %(security_system)s, %(property_company)s," \
                                                " %(public_transport)s, %(picture_urls)s,  %(created_at)s," \
                                                " %(updated_at)s)"
        print(sql)
        try:
            # 执行sql语句
            if sql_type == 'update':
                cursor.execute(sql)
            else:
                cursor.executemany(sql, args)
            # 执行sql语句
            db.commit()
        except Exception as e:
            # 发生错误时回滚
            db.rollback()
            print('插入失败')
            print(e)
        finally:
            # 关闭数据库连接
            db.close()
