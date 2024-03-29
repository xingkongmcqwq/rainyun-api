#导入库
import requests
import json
import os
#声明版本
version = '1.4'
#检测更新
try:
    url = "http://api.v2.imxingkong.top:8000/update/"
    update = requests.request("GET", url)
    update_json = update.json()
    if update_json['version'] != version:
        print(f'有新版本：{update_json["version"]},当前版本{version}')
    else:
        print(f'已是最新版，当前版本{version}')
except:
    print(f'连接服务器失败，当前版本{version}')
print('==============================')
# 检测并创建API默认文件夹
config_dir = 'config'
if not os.path.isdir(config_dir):
    os.makedirs(config_dir)
    print('配置文件夹已创建，请修改config目录里的key.json')
# 检测并创建API默认文件
key_file_path = os.path.join(config_dir, 'key.json')
if not os.path.isfile(key_file_path):
    with open(key_file_path, 'w') as json_cj:
        json_cj.write('''{"api_key":""}''')
        print('已创建key.json文件，请在其中填写API密钥')
#Api信息
with open('config/key.json') as key_json:
    key_json_tmp = json.load(key_json)
api_key = key_json_tmp['api_key']
if api_key == '':
    print('请填写API密钥')
    print('Powered by xingkongqwq')
    exit()
else:
    pass
#请求用户信息
url = "https://api.v2.rainyun.com/user/"
payload={}
headers_yh = {
   'X-Api-Key': api_key
}
res_points = requests.request("GET", url, headers=headers_yh, data=payload)
zh_json = res_points.json()
##print(zh_json)
points = zh_json['data']['Points']
ID = zh_json['data']['ID']
name = zh_json['data']['Name']
print(f'ID：{ID}')
print(f'用户名：{name}')
print(f'剩余积分：{points}')
print('==============================')
#签到部分
url_lqjf = 'https://api.v2.rainyun.com/user/reward/tasks'
headers_lqjf = {
    'content-type':"application/json",
    'X-Api-Key':api_key
    }
body_lqjf = {
    "task_name" : '每日签到',
    "verifyCode" : ''
    }
res_lqjf = requests.request("POST", url_lqjf, headers=headers_lqjf, data = json.dumps(body_lqjf))
tmp_lqjf = res_lqjf.json()
try:
    if tmp_lqjf['data'] == 'ok':
        print(f'签到成功，当前剩余积分：{points + 300}')
except:
    if tmp_lqjf['code'] == 30011:
        print(f'签到失败')
print('==============================')
#自动申请提现部分
url_zdtx = 'https://api.v2.rainyun.com/user/reward/withdraw'
headers_zdtx = {
    'content-type':"application/json",
    'X-Api-Key':api_key
    }
body_zdtx = {
    "points": points,
    "target": api_key
    }
if points >= 60000:
    res_zdtx = requests.request("POST", url_zdtx, headers=headers_zdtx, data = json.dumps(body_zdtx))
    print(f'自动提现成功')
else:
    print(f'自动提现失败，当前积分：{points}')
print('==============================')
#提现列表部分
#输入你的options
options='{"columnFilters":{},"sort":[],"page":1,"perPage":20}'
url_txsq = 'https://api.v2.rainyun.com/user/reward/withdraw?options='+options
headers_txsq = {
    'content-type':"application/json",
    'X-Api-Key':api_key
    }
res_txsq = requests.request("GET", url_txsq, headers=headers_txsq)
txsq_json = res_txsq.json()
tmp_1 = txsq_json['data']
tmp_2 = tmp_1['Records']
#是否提现判断并输出
try:
    tmp_3 = tmp_2[0]
    if tmp_3["status"] == 'finished':
        print('上一次提现记录：')
        print(f'提现ID：{tmp_3["id"]}')
        print(f'提现账户：{tmp_3["account"]}')
        print(f'提现方式：{tmp_3["target"]}')
        print(f'提现积分：{tmp_3["points"]}')
        print(f'提现金额：{tmp_3["money"]}')
        print(f'提现状态：{tmp_3["status"]}')
    else:
        print('本次提现记录：')
        print(f'提现ID：{tmp_3["id"]}')
        print(f'提现账户：{tmp_3["account"]}')
        print(f'提现方式：{tmp_3["target"]}')
        print(f'提现积分：{tmp_3["points"]}')
        print(f'提现金额：{tmp_3["money"]}')
        print(f'提现状态：{tmp_3["status"]}')
except:
    print('没有提现记录')
#其它
print('Powered by xingkongqwq')
