from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import json
import urllib.request
from urllib.parse import urlencode

music = on_command("新闻",priority=3)
@music.handle()
async def test_handle(bot: Bot, event: Event, state: T_State):
    groupid=event.group_id
    url = 'https://api.iyk0.com/ysxw/'
    msg=event.get_message
    data = msg()
    f = urllib.request.urlopen(url)
    nowapi_call = f.read()
    a_result = json.loads(nowapi_call)
    print(type(a_result))
    if 'code' in a_result:
        a_sum = a_result['sum']
        if a_sum > 10:
            a_sum = 10
        b_sum=0
        while b_sum != a_sum:
            print(b_sum)
            print(a_result['data'][b_sum]['image'])
            print(a_result['data'][b_sum]['title'])
            sendmessage_a='[CQ:image,file={}]'.format(a_result["data"][b_sum]['image'])
            sendmessage_b=a_result['data'][b_sum]['title']
            sendmessage_c=a_result['data'][b_sum]['url']
            sendmessage = sendmessage_a+sendmessage_b+sendmessage_c

            print(type(sendmessage))
            await bot.call_api("send_msg",**{'message_type':"group","group_id":groupid,"message":sendmessage})
            b_sum = b_sum + 1
