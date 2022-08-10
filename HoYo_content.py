import requests  #リクエストの際に利用
import time  #リクエストする時間を調整するのに利用
import json  #json形式に利用
import pprint
import re


def comment(post_id):
    headers = {"content-type": "application/json", "x-rpc-language": "ja-jp"}

    params = {'is_hot': "true", 'post_id': post_id, 'size': 15}
    is_last = False

    datas = []
    data = {}
    
    while not is_last:
        response = requests.get(
            'https://bbs-api-os.hoyolab.com/community/post/wapi/getPostReplies',
            params=params,
            headers=headers)

        res = response.json()

        for list in res["data"]["list"]:

            tag_content = re.compile('<.*?>')
            cleantext = re.sub(tag_content, '', list["reply"]["content"])
            data["comment"] = cleantext
            data["floor_id"] = list["reply"]["floor_id"]
            data["created_at"] = list["reply"]["created_at"]
            data["nickname"] = list["user"]["nickname"]
            data["avatar_url"] = list["user"]["avatar_url"]
            data["uid"] = list["user"]["uid"]
            data["like_num"] = list["stat"]["like_num"]
            data["select"] = "親コメント"

            datas.append(data)
            data = {}
            
            if list["stat"]["sub_num"] > 0:
                subcomment_data = subcomment(post_id,list["reply"]["floor_id"])
                datas.extend(subcomment_data)

        print("親コメント",len(datas))
        params["last_id"] = res["data"].get("last_id", None)
        is_last = res["data"]["is_last"]

    return datas

def subcomment(post_id,floor_id):
    headers = {"content-type": "application/json", "x-rpc-language": "ja-jp"}

    params = {
        'floor_id': floor_id, 
        'post_id': post_id, 
        'size': 15
    }
    is_last = False

    datas = []
    data = {}
    
    while not is_last:
        response = requests.get(
            'https://bbs-api-os.hoyolab.com/community/post/wapi/getSubReplies',
            params=params,
            headers=headers)
        
        res = response.json()

        for list in res["data"]["list"]:

            tag_content = re.compile('<.*?>')
            cleantext = re.sub(tag_content, '', list["reply"]["content"])
            data["comment"] = cleantext
            data["created_at"] = list["reply"]["created_at"]
            data["nickname"] = list["user"]["nickname"]
            data["avatar_url"] = list["user"]["avatar_url"]
            data["uid"] = list["user"]["uid"]
            data["like_num"] = list["stat"]["like_num"]
            data["select"] = "子コメント"

            datas.append(data)
            data = {}

        print("子コメント",len(datas))
        params["last_id"] = res["data"].get("last_id", None)
        is_last = res["data"]["is_last"]

    return datas