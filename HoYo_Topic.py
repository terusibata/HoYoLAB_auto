import requests  #リクエストの際に利用
import time  #リクエストする時間を調整するのに利用
import json  #json形式に利用
import pprint


def trends(topic_id=None, count=15):
    if not topic_id:
        return None

    if count % 15 != 0:
        count = 15

    headers = {"content-type": "application/json", "x-rpc-language": "ja-jp"}
    for_count = int(count / 15)

    datas = []
    data = {}
    params = {
        'gids': 2,
        'loading_type': 0,
        'page_size': 15,
        'reload_times': 0,
        'topic_id': topic_id
    }

    for reload_count in range(for_count):

        params["reload_times"] = reload_count

        response = requests.get(
            'https://bbs-api-os.hoyolab.com/community/post/wapi/topic/post/list',
            params=params,
            headers=headers)

        res = response.json()

        for list in res["data"]["posts"]:
            data["post_id"] = list["post"]["post_id"]
            data["uid"] = list["post"]["uid"]
            data["title"] = list["post"]["subject"]
            data["created_at"] = list["post"]["created_at"]
            data["nickname"] = list["user"]["nickname"]
            data["icon"] = list["user"]["avatar_url"]
            data["view_num"] = list["stat"]["view_num"]
            data["reply_num"] = list["stat"]["reply_num"]
            data["like_num"] = list["stat"]["like_num"]

            try:
                topics = []
                topic = {}
                for topic_list in list["topics"]:
                    topic["name"] = topic_list["name"]
                    topics.append(topic)
                    topic = {}

                data["topics"] = topics
            except:
                data["topics"] = []

            datas.append(data)
            data = {}

        params["last_id"] = res["data"]["last_id"]
        params["loading_type"] = 1

    return datas


def new(topic_id=None, count=15):
    if not topic_id:
        return None

    if count % 15 != 0:
        count = 15

    headers = {"content-type": "application/json", "x-rpc-language": "ja-jp"}
    for_count = int(count / 15)

    datas = []
    data = {}
    params = {
        'gids': 2,
        'loading_type': 0,
        'page_size': 15,
        'reload_times': 0,
        'topic_id': topic_id
    }

    for reload_count in range(for_count):

        params["reload_times"] = reload_count

        response = requests.get(
            'https://bbs-api-os.hoyolab.com/community/painter/wapi/topic/post/new',
            params=params,
            headers=headers)

        res = response.json()

        for list in res["data"]["list"]:
            data["post_id"] = list["post"]["post_id"]
            data["uid"] = list["post"]["uid"]
            data["title"] = list["post"]["subject"]
            data["created_at"] = list["post"]["created_at"]
            data["nickname"] = list["user"]["nickname"]
            data["icon"] = list["user"]["avatar_url"]
            data["view_num"] = list["stat"]["view_num"]
            data["reply_num"] = list["stat"]["reply_num"]
            data["like_num"] = list["stat"]["like_num"]

            try:
                topics = []
                topic = {}
                for topic_list in list["topics"]:
                    topic["name"] = topic_list["name"]
                    topics.append(topic)
                    topic = {}

                data["topics"] = topics
            except:
                data["topics"] = []

            datas.append(data)
            data = {}

        params["last_id"] = res["data"]["last_id"]
        params["loading_type"] = 1

    return datas
