from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
#import asyncio
import json
import urllib.request
from urllib.parse import urlencode




#注册一个事件响应器，事件类型为command，
weather=on_command("获取天气",priority=10)

@weather.handle()


async def test_handle(bot: Bot, event: Event, state: T_State):
    
    groupid=event.group_id
    await bot.call_api("send_group_msg", **{"group_id": groupid, "message": "请输入城市（如“#厦门”“#武汉”）"})

@weather.got("city")
async def netdisk_out(bot: Bot, event: Event, state: T_State):
    groupid = event.group_id
    CITY = state["city"]
    if event.message_type == "group":
         url = 'https://api.iyk0.com/tq/?'
    params = {
        'city' : CITY,
        'type' : ''
        }
    params = urlencode(params)

    #1.f = urllib.request.urlopen('%s%s' % (url,params))
    #2.nowapi_call = f.read()
    #3.a_result = json.loads(nowapi_call)

    a_result = json.loads(urllib.request.urlopen('%s%s' % (url,params)).read())
    if 'code' in a_result:
        
        if a_result['code'] == 200:
            if 'wea' in a_result:
                img_weather = ''
                if a_result['wea'] == '晴':
                    img_weather = '☀️'
                elif a_result['wea'] == '多云':
                    img_weather = '⛅'
                elif a_result['wea'] == '阴':
                    img_weather = '☁️'
                elif a_result['wea'] == '小雨':
                    img_weather = '☂️'
                elif a_result['wea'] == '中雨':
                    img_weather = '🌧️'
                elif a_result['wea'] == '大雨':
                    img_weather = '🌧️🌧️'
                elif a_result['wea'] == '暴雨':
                    img_weather = '🌧️🌧️🌧️'
                elif a_result['wea'] == '雷阵雨':
                    img_weather = '⛈️'
                elif a_result['wea'] == '小雪':
                    img_weather = '🌨️'
                elif a_result['wea'] == '中雪':
                    img_weather = '🌨️'
                elif a_result['wea'] == '大雪':
                    img_weather = '🌨️🌨️'
                elif a_result['wea'] == '暴雪':
                    img_weather = '🌨️🌨️🌨️'
                elif a_result['wea'] == '雾':
                    img_weather = '🌫️'
                elif a_result['wea'] == '雷':
                    img_weather = '🌩️'    
                elif a_result['wea'] == '晴转雨':
                    img_weather = '🌦 '
            await bot.call_api("send_group_msg", **{"group_id": groupid, "message": a_result['city']+' '
                                                                                    +a_result['wea']+img_weather+'\n'
                                                                                    +"实时温度 "+a_result['tem']+'°C\n'
                                                                                    +"空气质量 " +a_result['air']+'\n'
                                                                                    +"风向 "+a_result['win']+'\n'
                                                                                    +"风力等级 "+a_result['win_speed']+'\n'
                                                                                    +"风速 " + a_result['win_meter'] +'\n'                                                                                    
                                                                                    +"最高温度 "+a_result['tem_day']+'°C\n'
                                                                                    +"最低温度 "+a_result['tem_night']+'°C\n'
                                                                                    +a_result['time']+'\n'                         
                                                                                    })
        elif a_result['code'] == 202 :
            print(a_result['code'])
            print(a_result['msg'])
            print(a_result)
            await bot.call_api("send_group_msg", **{"group_id": groupid, "message": "抱歉，没有找到所在城市的天气信息,连接已断开"})
        
