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



# 指令处理
command_handler = on_command("网盘资源", priority=10)

@command_handler.handle()
async def netdisk_out_menu(bot: Bot, event: Event, state: T_State):
    connect = sqlite3.connect(".\\Bot_data\\SQLite\\BaiduCloudDisk.db")
    # 创建游标
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM BAIDU")
    if event.message_type == "group":
        group_id = event.group_id
        msg = "网盘资源菜单如下： \n"
        for info in cursor:
            msg = msg + str(info[0]) + ".  "
            msg = msg + info[1] + "\n"
        msg = msg + "\n请输入对应序号获取资源"
        await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
    cursor.close()
    connect.commit()
    connect.close()


@command_handler.got("ID")
async def netdisk_out(bot: Bot, event: Event, state: T_State):
    group_id = event.group_id
    ID = state["ID"]
    if event.message_type == "group":
        if not ID.isdigit():
            msg = "请发送正确的数字! 连接已断开"
            await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
            return
        else:
            connect = sqlite3.connect(".\\Bot_data\\SQLite\\BaiduCloudDisk.db")
            # 创建游标
            cursor = connect.cursor()
            ID = int(ID)
            id_tuple = (ID,)
            cursor.execute('''
                            SELECT * FROM BAIDU
                            WHERE ID=(?)''',id_tuple)
            if not len(list(cursor)):
                msg = "没有查询到相关资源！"
                await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
            cursor.execute('''
                                        SELECT * FROM BAIDU
                                        WHERE ID=(?)''', id_tuple)
            for info in cursor:
                msg = ""
                msg = msg + str(info[0]) + ".  "
                msg = msg + info[1] + ": \n"
                msg = msg + "类型： " + info[6] + "\n"
                msg = msg + "网盘链接： " + info[2] + "\n"
                msg = msg + "提取码： " + info[3] + "\n"
                msg = msg + "解压密码： " + info[4] + "\n"
                msg = msg + "INFO： " + info[5] + "\n"
                await bot.call_api("send_group_msg", **{"group_id": group_id, "message": msg})
            cursor.close()
            connect.commit()
            connect.close()







