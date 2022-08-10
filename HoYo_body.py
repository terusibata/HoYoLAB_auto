import requests  #リクエストの際に利用
import time  #リクエストする時間を調整するのに利用
import json  #json形式に利用
import pprint
import ast


def body(post_id=None):
    headers = {"content-type": "application/json", "x-rpc-language": "ja-jp"}

    params = {'post_id': post_id, 'read': 1}
    response = requests.get(
        'https://bbs-api-os.hoyolab.com/community/post/wapi/getPostFull',
        params=params,
        headers=headers)

    res = response.json()

    view_type = res["data"]["post"]["post"]["view_type"]

    if view_type == 1:
        return view_type_1(res)
    elif view_type == 2:
        return view_type_2(res)
    elif view_type == 5:
        return view_type_5(res)
    elif view_type == 6:
        return view_type_6(res)
    else:
        print(view_type)


def view_type_1(res):
    data = {}

    data["title"] = res["data"]["post"]["post"]["subject"]
    data["post_id"] = res["data"]["post"]["post"]["post_id"]
    data["uid"] = res["data"]["post"]["post"]["uid"]
    data["view_type"] = res["data"]["post"]["post"]["view_type"]

    body_datas = []
    body_data = {}

    body = res["data"]["post"]["post"]["structured_content"]
    body = pretty_json(body)
    # print(ast.literal_eval(body))

    for contents in body:
        try:
            if isinstance(contents["insert"], dict):
                if "image" in contents["insert"].keys():
                    body_data["type"] = "image"
                    body_data["link"] = contents["insert"]["image"]
                elif "emoticon" in contents["insert"].keys():
                    body_data["type"] = "emoticon"
                    body_data["link"] = contents["insert"]["emoticon"]["url"]
                elif "divider" in contents["insert"].keys():
                    body_data["type"] = "divider"
                elif "video" in contents["insert"].keys():
                    body_data["type"] = "video"
                    body_data["link"] = contents["insert"]["video"]
                elif "vote" in contents["insert"].keys():
                    #アンケートフォームの場合
                    body_data["type"] = "vote"

                    headers = {
                        "content-type": "application/json", 
                        "x-rpc-language": "ja-jp"
                    }
                    params = {
                        'owner_uid': contents["insert"]["vote"]["uid"], 
                        'vote_ids': contents["insert"]["vote"]["id"]
                    }
                    response = requests.get('https://bbs-api-os.hoyolab.com/community/post/api/getVotes',params=params,headers=headers)

                    res = response.json()
                    vote_res = res["data"]["data"][0]
                    vote_data = {}
                    vote_data["title"] = vote_res["title"]
                    vote_data["option"] = vote_res["vote_option_indexes"]

                    body_data["content"] = vote_data
                else:
                    print(contents["insert"])
            else:
                if "attributes" in contents.keys() and "link" in contents["attributes"].keys():
                    body_data["type"] = "link"
                    body_data["link"] = contents["attributes"]["link"]
                    body_data["content"] = contents["insert"]
                else:
                    body_data["type"] = "text"
                    body_data["content"] = contents["insert"]

            body_datas.append(body_data)
            body_data = {}
        except:
            body_data = {}
            #print(contents)
            continue

    data["body"] = body_datas

    return data


def view_type_2(res):
    data = {}

    data["title"] = res["data"]["post"]["post"]["subject"]
    data["post_id"] = res["data"]["post"]["post"]["post_id"]
    data["uid"] = res["data"]["post"]["post"]["uid"]
    data["view_type"] = res["data"]["post"]["post"]["view_type"]

    body_datas = {}

    body = res["data"]["post"]["post"]["content"]
    body = pretty_json(body)
    # print(ast.literal_eval(body))

    body_datas["describe"] = body["describe"]

    body_url_list = []
    for img_url in body["imgs"]:
        body_url_list.append(img_url)

    body_datas["imgs"] = body_url_list

    data["body"] = body_datas

    return data


def view_type_5(res):
    data = {}

    data["title"] = res["data"]["post"]["post"]["subject"]
    data["post_id"] = res["data"]["post"]["post"]["post_id"]
    data["uid"] = res["data"]["post"]["post"]["uid"]
    data["view_type"] = res["data"]["post"]["post"]["view_type"]

    body_datas = {}

    body = res["data"]["post"]["post"]["content"]
    body = pretty_json(body)
    # print(ast.literal_eval(body))

    body_datas["describe"] = body["describe"]
    body_datas["video"] = body["video"]

    data["body"] = body_datas

    return data

def view_type_6(res):
    data = {}

    data["title"] = res["data"]["post"]["post"]["subject"]
    data["post_id"] = res["data"]["post"]["post"]["post_id"]
    data["uid"] = res["data"]["post"]["post"]["uid"]
    data["view_type"] = res["data"]["post"]["post"]["view_type"]

    body_datas = {}

    body = res["data"]["post"]["post"]["content"]
    body = pretty_json(body)

    body_datas["topic_id"] = body["topic"]["topic_id"]
    body_datas["topic_name"] = body["topic"]["topic_name"]
    body_datas["topic_content"] = body["topic"]["content"]
    body_datas["img"] = body["photo"]["url"]
    body_datas["cover"] = body["cover"]["url"]

    data["body"] = body_datas

    return data

def pretty_json(obj):
    temp = json.loads(obj) if isinstance(obj, str) else obj
    return temp
