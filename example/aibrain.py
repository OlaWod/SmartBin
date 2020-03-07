import json
import urllib.request


# 思知机器人 API
ROBOT_KEY = "06eccece6059f8ce0a1ad004a8dd2485"
API_URL = "https://api.ownthink.com/bot"


# 思知机器人处理
def ai_think(user_text):

    req = {
        "spoken": user_text,
        "appid": ROBOT_KEY,
        "userid": "dad"
    }
    # 将字典格式的req编码为utf8
    req = json.dumps(req).encode('utf8')
    

    http_post = urllib.request.Request(API_URL, data=req, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(http_post)
    response_str = response.read().decode('utf8')
    response_dic = json.loads(response_str)
    

    ai_text = response_dic['data']['info']['text']
    print("AI说: " + ai_text)

    return ai_text


if __name__=='__main__':    # 模块测试
    print(ai_think('明天天气如何'))
