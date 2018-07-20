import requests
import itchat
import time
from threading import Timer

KEY = '2a581c166755433f830dd6f4eb8a4fdb'

def get_response(msg):
    # 构造发送给图灵机器人服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return

def isMsgFromMyself(msgFromUserName):
    # 检查消息发送方是否为自己
    global myName
    return myName == msgFromUserName


# 注册文本消息回复函数
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    global autoReplyFlag,  timerSet, noReply, t  # 状态标志位
    print(msg['Text'])
    if isMsgFromMyself(msg['FromUserName']):
        print("Replied!!")
        autoReplyFlag = False
        noReply = False
        try:
            t.cancel()
            print("Timer Canceled")
            timerSet = False
        except:
            pass
        return None

    if autoReplyFlag:
        # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
        defaultReply = 'I received: ' + msg['Text']
        # 如果图灵Key出现问题，那么reply将会是None
        reply = get_response(msg['Text'])
        # a or b的意思是，如果a有内容，那么返回a，否则返回b
        # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
        return reply or defaultReply
    else:
        noReply = True
        if not timerSet:
            # if time.time()-noReplyStartTime >= 120:
            print("Timer setting")
            t = Timer(12, sendBusyStatus, [msg['FromUserName']])
            t.start()
            timerSet = True

def sendBusyStatus(UserName):
    global noReply, autoReplyFlag, timerSet
    print("Timer Working!")
    if noReply:
        itchat.send("我的主人在认真地熵减！让我先陪你聊一会吧", UserName)
        autoReplyFlag = True
        timerSet = False

# 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
itchat.auto_login()

autoReplyFlag, timerSet, noReply = False, False, False
t = 0  # 定义全局变量t, 用作触发器使用，此行甚是丑陋；怎么才能更优雅呢？请大神指点。
myName = itchat.get_friends(update=True)[0]['UserName']
itchat.run()

#作者：NoneLand
#链接：https://www.jianshu.com/p/1b6e3636fa50
#來源：简书
#简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。