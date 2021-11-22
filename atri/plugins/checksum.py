from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import random
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from pillow_trans import image_call

#注册一个事件响应器，事件类型为command，
checksum=on_command("随机验证码",priority=3)

@checksum.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
    groupid=event.group_id
    image_call(4,1,'随机验证码')
    sndmsg=".\\Bot_data\\IMAGE\\code.png"
    await bot.call_api("send_msg",**{"message_type":"group","group_id":groupid,"message":"[CQ:image,file=file:///{}]".format(sndmsg)})