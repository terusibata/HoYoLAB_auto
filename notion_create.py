import requests
from pprint import pprint
import time
import os
import datetime

class OneselfError(Exception):
    """自作プログラムのエラーを知らせる例外クラスです。"""
    pass


def get_request_url(end_point):
    return f'https://api.notion.com/v1/{end_point}'

def notion_request(url_data,method,json_data):
    count = 0
    while True:
        try:
            requests.request(
                    method,
                    url=get_request_url(url_data),
                    headers=headers,
                    json=json_data)
            break
        except:
            count = count + 1
            print(f"{count}回目のエラーが発生しました")
            if count >= 5:
                print("requestをスルーしました")
                break
        
    


notion_api_key = os.environ['notion_api_key']

headers = {
    "Authorization": f"Bearer {notion_api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}


class block():
    def heading_2(block_id=None, content_text=None):
        create_json = {
            "children": [{
                "object": 'block',
                "type": 'heading_2',
                "heading_2": {
                    "rich_text": [
                        {
                            "type": 'text',
                            "text": {
                                "content": content_text,
                            },
                        },
                    ],
                },
            }]
        }
        notion_request(f'blocks/{block_id}/children','patch',create_json)
        time.sleep(0.3)
        print("ヘッダー2入力完了")

    def text(block_id=None, content_text=None):
        create_json = {
            "children": [{
                "object": 'block',
                "type": 'paragraph',
                "paragraph": {
                    "rich_text": [
                        {
                            "type": 'text',
                            "text": {
                                "content": content_text,
                            },
                        },
                    ],
                },
            }]
        }
        notion_request(f'blocks/{block_id}/children','patch',create_json)
        time.sleep(0.3)
        print("テキスト入力完了")

    def link_text(block_id=None, content_text=None, link=None):
        create_json = {
            "children": [{
                "object": 'block',
                "type": 'paragraph',
                "paragraph": {
                    "rich_text": [
                        {
                            "type": 'text',
                            "text": {
                                "content": content_text,
                                "link": {
                                    "url": link
                                }
                            },
                        },
                    ],
                },
            }]
        }
        notion_request(f'blocks/{block_id}/children','patch',create_json)
        time.sleep(0.3)
        print("リンクテキスト入力完了")

    def divider(block_id=None):
        create_json = {
            "children": [{
                "object": 'block',
                "type": 'divider',
                "divider": {}
            }]
        }
        notion_request(f'blocks/{block_id}/children','patch',create_json)
        time.sleep(0.3)
        print("区切り線の書き込み完了")

    def image(block_id=None, img=None):
        create_json = {
            "children": [{
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {
                        "url": img
                    }
                }
            }]
        }
        notion_request(f'blocks/{block_id}/children','patch',create_json)
        time.sleep(0.3)
        print("画像の埋め込み完了")

    def Video(block_id=None, Video=None):
        create_json = {
            "children": [{
                "type": "video",
                "video": {
                    "type": "external",
                    "external": {
                        "url": Video
                    }
                }
            }]
        }
        notion_request(f'blocks/{block_id}/children','patch',create_json)
        time.sleep(0.3)
        print("ビデオの埋め込み完了")

    def embed(block_id=None, url=None):
        create_json = {"children": [{"type": "embed", "embed": {"url": url}}]}
        notion_request(f'blocks/{block_id}/children','patch',create_json)
        time.sleep(0.3)
        print("埋め込み完了")

class date_database():
    def database(block_id=None, content_text=None):
        create_json = {
            "parent": {
                "type": "page_id",
                "page_id": block_id
            },
            "icon": {
                "type": "emoji",
                "emoji": "📝"
            },
            "title": [{
                "type": "text",
                "text": {
                    "content": content_text,
                    "link": None
                }
            }],
            "properties": {
                "ページタイトル": {
                    "title": {}
                },
                "作成者": {
                    "created_by": {}
                },
                "作成日": {
                    "created_time": {}
                }
            }
        }
        response = requests.request('post',
                                    url=get_request_url('databases'),
                                    headers=headers,
                                    json=create_json)
        #pprint(response.json())
        time.sleep(0.3)
        print(f'{response.json()["id"]}にデータベースを作成しました')
        return response.json()["id"]

    def database_page(block_id=None, page_title=None):
        create_json = {
            "parent": {
                "database_id": block_id
            },
            "icon": {
                "emoji": "📝"
            },
            "properties": {
                "ページタイトル": {
                    "title": [{
                        "text": {
                            "content": page_title
                        }
                    }]
                }
            }
        }
        response = requests.request('post',
                                    url=get_request_url('pages'),
                                    headers=headers,
                                    json=create_json)
        time.sleep(0.3)
        print(f'{block_id }のデータベースに新しいページを作成しました')
        return response.json()["id"]


class comment_database():
    def database(block_id=None, content_text=None):
        create_json = {
            "parent": {
                "type": "page_id",
                "page_id": block_id
            },
            "icon": {
                "external": {
                    "url": "https://www.notion.so/icons/chat_blue.svg"
                }
            },
            "title": [{
                "type": "text",
                "text": {
                    "content": content_text,
                    "link": None
                }
            }],
            "properties": {
                "コメント": {
                    "title": {}
                },
                "いいね数": {
                    "number": {
                        "format": "number"
                    }
                },
                "投稿日時": {
                    "date": {}
                },
                "ニックネーム": {
                    "rich_text": {}
                },
                "プロフィール": {
                    "url": {}
                },
                "コメントの種類": {
                    "select": {
                        "options": [{
                            "name": "親コメント",
                            "color": "red"
                        }, {
                            "name": "子コメント",
                            "color": "yellow"
                        }]
                    }
                }
            }
        }
        response = requests.request('post',
                                    url=get_request_url('databases'),
                                    headers=headers,
                                    json=create_json)
        #pprint(response.json())
        time.sleep(0.3)
        print(f'{response.json()["id"]}にデータベースを作成しました')
        return response.json()["id"]

    def database_page(block_id=None, comment_data=None):

        comment_data["created_at"] = str(datetime.datetime.fromtimestamp(comment_data["created_at"])).replace(' ', "T")+"+09:00"

        create_json = {
            "parent": {
                "database_id": block_id
            },
            "icon": {
                "type": "external",
                "external": {
                    "url": comment_data["avatar_url"]
                }
            },
            "properties": {
                "コメント": {
                    "title": [{
                        "text": {
                            "content": comment_data["comment"]
                        }
                    }]
                },
                "いいね数": {
                    "number": comment_data["like_num"]
                },
                "投稿日時": {
                    "date": {
                        "start": comment_data["created_at"]
                    }
                },
                "ニックネーム": {
                    "rich_text": [{
                        "text": {
                            "content": comment_data["nickname"]
                        }
                    }]
                },
                "プロフィール": {
                    "url": "https://www.hoyolab.com/accountCenter/postList?id=" + comment_data["uid"]
                },
                "コメントの種類": {
                    "select": {
                        "name": comment_data["select"]
                    }
                }
            }
        }
        try:
            requests.request(
                'post',
                url=get_request_url('pages'),
                headers=headers,
                json=create_json
            )
        except:
            print("コメントの追加に失敗しました")
        #pprint(response.json())
        time.sleep(0.3)


class topic_database():
    def database(block_id=None, content_text=None, icon_url=None):
        create_json = {
            "parent": {
                "type": "page_id",
                "page_id": block_id
            },
            "icon": {
                "external": {
                    "url": icon_url
                }
            },
            "title": [{
                "type": "text",
                "text": {
                    "content": content_text,
                    "link": None
                }
            }],
            "properties": {
                "タイトル": {
                    "title": {}
                },
                "ページURL": {
                    "url": {}
                },
                "投稿日時": {
                    "date": {}
                },
                "ニックネーム": {
                    "rich_text": {}
                },
                "閲覧数": {
                    "number": {
                        "format": "number"
                    }
                },
                "いいね数": {
                    "number": {
                        "format": "number"
                    }
                },
                "コメント数": {
                    "number": {
                        "format": "number"
                    }
                },
                "トピック": {
                    "type": "multi_select",
                    "multi_select": {}
                }
            }
        }
        response = requests.request('post',
                                    url=get_request_url('databases'),
                                    headers=headers,
                                    json=create_json)
        time.sleep(0.3)
        print(f'{response.json()["id"]}にデータベースを作成しました')
        return response.json()["id"]

    def database_page(block_id=None, topic_data=None):

        topic_data["created_at"] = str(datetime.datetime.fromtimestamp(topic_data["created_at"])).replace(' ', "T")+"+09:00"

        create_json = {
            "parent": {
                "database_id": block_id
            },
            "icon": {
                "type": "external",
                "external": {
                    "url": topic_data["icon"]
                }
            },
            "properties": {
                "タイトル": {
                    "title": [{
                        "text": {
                            "content": topic_data["title"]
                        }
                    }]
                },
                "ページURL": {
                    "url": "https://www.hoyolab.com/article/" + topic_data["post_id"]
                },
                "投稿日時": {
                    "date": {
                        "start": topic_data["created_at"]
                    }
                },
                "ニックネーム": {
                    "rich_text": [{
                        "text": {
                            "content": topic_data["nickname"]
                        }
                    }]
                },
                "閲覧数": {
                    "number": topic_data["view_num"]
                },
                "いいね数": {            
                  "number": topic_data["like_num"]
                },
                "コメント数": {
                  "number": topic_data["reply_num"]
                },
        		"トピック": {
        			"multi_select": topic_data["topics"]
                }
            }
        }
        try:
            response = requests.request('post',
                                        url=get_request_url('pages'),
                                        headers=headers,
                                        json=create_json)
        except Exception as e:
            print(e)
        #pprint(response.json())
        time.sleep(0.3)
        try:
            response_id = response.json()["id"]
            print(f'{block_id }のデータベースに新しいページを作成しました')
        except:
            response_id = None
            print("アップロードに失敗しました")
            pprint(response)
        return response_id
