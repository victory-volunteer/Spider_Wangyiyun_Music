import execjs
import json
import requests


def js_from_file(file_name):
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()
    return result


def create_arguments(id, cursor):
    data = {
        "rid": f"R_SO_4_{id}",
        "threadId": f"R_SO_4_{id}",
        "pageNo": "1",
        "pageSize": "20",
        "cursor": cursor,
        "offset": "0",
        "orderType": "1",
        "csrf_token": ""
    }
    arguments1 = json.dumps(data).replace(' ', '')
    context1 = execjs.compile(js_from_file('./arguments.js'))
    result1 = context1.call("getkey", arguments1)
    return result1


def listen_comment(params, encSecKey):
    url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'referer': 'https://music.163.com/',
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'params': params,
        'encSecKey': encSecKey
    }
    response = requests.post(url, data=data, headers=headers)
    resp = response.json()
    datas = resp['data']['comments']
    if len(datas) == 0:
        return
    for data in datas:
        print(data['content'])
    cursor = resp['data']['cursor']
    return cursor


if __name__ == '__main__':
    id = 802418  # 歌曲id(评论数少)
    cursor = -1
    while True:
        result1 = create_arguments(id, cursor)
        cursor = listen_comment(result1['encText'], result1['encSecKey'])
        if cursor == None:
            break
        print('-' * 30)  # 用来标记每一页评论