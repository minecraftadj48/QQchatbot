from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.permission import *
from nonebot.adapters import Bot ,Event
from nonebot import on_command


matcher=on_command("测试",permission=SUPERUSER,priority=10)

@matcher.handle()
async def _(bot: Bot):
    await matcher.send("超管命令测试成功")


@matcher.got("key1", "超管提问")
async def _(bot: Bot, event: Event):
    await matcher.send("超管命令got成功")
