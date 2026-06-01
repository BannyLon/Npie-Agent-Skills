import requests
import json

def get_access_token(appid, secret):
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}"
    response = requests.get(url)
    return response.json().get('access_token')

def upload_draft(access_token, title, content, digest=""):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    data = {
        "articles": [
            {
                "title": title,
                "content": content,
                "digest": digest,
                "need_open_comment": 1
            }
        ]
    }
    response = requests.post(url, json=data)
    return response.json()
