# -*- coding:utf-8 -*-
import nonebot
from nonebot import require
import sqlite3
import asyncio
from nonebot import on_command
from nonebot import on_notice
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event

# 定时器
scheduler = require("nonebot_plugin_apscheduler").scheduler
# 群事件处理
group_handler = on_notice(priority=15)
# 指令处理
command_handler = on_command("用户刷新",priority=10)

# 定期更新数据库
@scheduler.scheduled_job("cron", hour="00", minute="00")
async def update_usersdata():
    # 传入bot对象
    bot = nonebot.get_bot()
    # 连接数据库
    connect = sqlite3.connect(".\\Bot_data\\SQLite\\Users.db")
    # 创建游标
    cursor = connect.cursor()
    # 遍历群组
    groups = await bot.call_api("get_group_list")
    for group in groups:
        group_id = group["group_id"]
        group_members = await bot.call_api("get_group_member_list", **{"group_id": group_id})
        for group_member in group_members:
            member_id = group_member["user_id"]
            # 将member_id放入元组中进行数据传入
            member_id_tuple=(member_id,)
            member_name = group_member["nickname"]
            cursor.execute("SELECT COUNT(*) FROM BASE WHERE QID=(?);",member_id_tuple)
            for c in cursor:
                if c[0] == 0:
                    insert_value = (member_id, member_name)
                    connect.execute('''
                                    INSERT INTO 
                                    BASE(PERMISSION,ATTITUDE,GOLD,QID,QQNAME) 
                                    VALUES(2,0,0,?,?);
                                    ''', insert_value)
    cursor.close()
    connect.commit()
    connect.close()


# 当群内新增成员时进行处理
@group_handler.handle()
async def add_member_to_user_database(bot: Bot, event: Event, state: T_State):
    if event.notice_type == 'group_increase':
        # 群号
        group_id = event.group_id
        # 进群者QQ号 QQ名
        member_id = event.user_id
        # 将member_id放入元组中进行数据传入
        member_id_tuple = (member_id,)
        info = await bot.call_api("get_group_member_info", **{"group_id": group_id,"user_id":member_id})
        member_name = info["nickname"]
        # 连接数据库
        connect = sqlite3.connect(".\\Bot_data\\SQLite\\Users.db")
        # 创建游标
        cursor = connect.cursor()
        # 判断是否已在数据库内
        cursor.execute("SELECT COUNT(*) FROM BASE WHERE QID=(?);",member_id_tuple)
        for c in cursor:
            if c[0] == 0:
                # 将用户添加入数据库
                insert_value = (member_id, member_name)
                connect.execute('''
                                                    INSERT INTO 
                                                    BASE(PERMISSION,ATTITUDE,GOLD,QID,QQNAME) 
                                                    VALUES(2,0,0,?,?);
                                                    ''', insert_value)
        cursor.close()
        connect.commit()
        connect.close()

# 接收指令进行刷新
@command_handler.handle()
async def refresh_user_database(bot: Bot, event: Event, state: T_State):
    # 连接数据库
    connect = sqlite3.connect(".\\Bot_data\\SQLite\\Users.db")
    # 创建游标
    cursor = connect.cursor()
    #权限审查
    caller = event.user_id
    caller = (caller,)
    cursor.execute("SELECT COUNT(*) FROM BASE WHERE QID=(?);",caller)
    #检查是否在数据库中
    for c in cursor:
        if c[0] == 0:
            return
        else:
            #检查是否满足权限
            cursor.execute("SELECT PERMISSION FROM BASE WHERE QID=(?)",caller)
            for c in cursor:
                if not c[0] == 0:
                    return
    # 遍历群组
    groups = await bot.call_api("get_group_list")
    for group in groups:
        group_id = group["group_id"]
        group_members = await bot.call_api("get_group_member_list", **{"group_id": group_id})
        for group_member in group_members:
            member_id = group_member["user_id"]
            # 将member_id放入元组中进行数据传入
            member_id_tuple = (member_id,)
            member_name = group_member["nickname"]
            cursor.execute("SELECT COUNT(*) FROM BASE WHERE QID=(?);",member_id_tuple)
            for c in cursor:
                if c[0] == 0:
                    insert_value = (member_id, member_name)
                    connect.execute('''
                                    INSERT INTO 
                                    BASE(PERMISSION,ATTITUDE,GOLD,QID,QQNAME) 
                                    VALUES(2,0,0,?,?);
                                    ''', insert_value)
    #
    cursor.close()
    connect.commit()
    connect.close()