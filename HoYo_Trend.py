import requests  #リクエストの際に利用
import time  #リクエストする時間を調整するのに利用
import json  #json形式に利用
import pprint


def trends(size=15):
    headers = {"content-type": "application/json", "x-rpc-language": "ja-jp"}

    params = {
        'gids': 2,
        'loading_type': 0,
        'page_size': size,
        'reload_times': 1,
    }
    response = requests.get(
        'https://bbs-api-os.hoyolab.com/community/painter/wapi/explore/topic/list',
        params=params,
        headers=headers)

    res = response.json()

    datas = []
    data = {}

    for list in res["data"]["list"]:
        data["id"] = list["base"]["id"]
        data["name"] = list["base"]["name"]
        data["cover_img"] = list["base"]["cover"]  #アイコン
        data["view_num"] = list["stat"]["view_num"]  #閲覧数
        data["post_num"] = list["stat"]["post_num"]  #投稿数
        data["member_num"] = list["stat"]["member_num"]  #メンバー数

        datas.append(data)
        data = {}

    return datas
