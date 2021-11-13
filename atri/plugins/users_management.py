import sqlite3

# 连接数据库
connect = sqlite3.connect("..\\..\\Bot_data\\SQLite\\Users.db")
# 创建游标
cursor = connect.cursor()
cursor.execute('''SELECT COUNT(*) FROM BASE WHERE QID=0;''')

