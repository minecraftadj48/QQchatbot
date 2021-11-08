# QQchatbot-manager

**预期实现的功能：** 基于go-cqhttp+nonebot2框架制作一个QQ群聊机器人的后台管理软件。具有插件管理、词库管理、后台数据库管理等功能。  
+ 通过插件管理，机器人可以集成图像匹配搜索、文字转语音、Pixiv关键字爬图、天气预报、群聊小游戏、群成员管理、群成员进群退群提示、签到、运势等功能。且相关的实现细节应该完全封装，用户只需要启用/卸载插件以及自定义插件相关参数即可。
+ 通过词库管理，机器人既可以通过一定的指令来学习新的词汇，也可以兼容网上现有的词库格式并能进行安装与卸载。
+ 通过后台数据库管理，可以在后台修改群聊用户的各项数据等  

**相关链接**  
[go-cqhttp文档](https://docs.go-cqhttp.org/)  
[nonebot2文档](https://v2.nonebot.dev/)

**网站wiki**  
[QQchabot-manager](https://亚托莉.com)

**一.词库格式**  
在bot初始化时，bot从/atri/Dictionary/index.json文件中读取词库文件的目录，先读取的词库文件**优先级更高**，不会被后读取的词库覆盖。index.json文件如下所示：  
    
    {
        "index":["atri\\Dictionary\\Genshin.json","atri\\Dictionary\\Base.json"]
    }
词库文件也为json格式，示例如下：

    {
        "刻晴今天吃什么":
            {
                "is_keyword":false,
                "need_at": false,
                "multi_reply": false,
                "reply": ["剑光如我，斩尽牛杂"],
                "need_attitude": 0
            },
        "可莉":
            {
                "is_keyword":false,
                "need_at": false,
                "multi_reply": true,
                "reply": ["哒哒哒","啦啦啦","蹦蹦炸弹","轰轰火花"],
                "need_attitude": 0
            }
    }
其中is_keyword意为关键字触发，即句子中只要        