# -*- coding:utf-8 -*-
import nonebot
from nonebot import require
import sqlite3
import asyncio
from nonebot import on_message
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
# 定时器
scheduler = require("nonebot_plugin_apscheduler").scheduler


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
            member_name = group_member["nickname"]
            cursor.execute("SELECT COUNT(*) FROM BASE WHERE QID={};".format(member_id))
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
