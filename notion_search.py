import requests
from pprint import pprint
import time
import os
import notion_create
import json

class OneselfError(Exception):
    """自作プログラムのエラーを知らせる例外クラスです。"""
    pass

def get_request_url(end_point):
    return f'https://api.notion.com/v1/{end_point}'

notion_api_key = os.environ['notion_api_key']

headers = {"Authorization": f"Bearer {notion_api_key}",
           "Content-Type": "application/json",
           "Notion-Version": "2022-02-22"}

def search_page(page_id=None,page_title=None):
  get_list = getpages(page_id)
  for get_data in get_list:
    if get_data["title"] == page_title:
      return get_data["id"]
  #同じタイトルがなかったらデータベース作成
  database_id = notion_create.date_database.database(page_id,page_title)
  return database_id

def search_database(page_id=None,page_title=None):
  get_list = getdatabase(page_id)
  for get_data in get_list:
    if get_data["title"] == page_title:
      return get_data["id"]
  #同じタイトルがなかったらページ作成
  database_id = notion_create.date_database.database_page(page_id,page_title)
  return database_id
  
def getpages(page_id=None):
  if not page_id:
    raise OneselfError("page_idが引数にありません")
  
  list = []
  datas = {}
  start_cursor = None
  
  while True:
    if start_cursor is None:
      response = requests.request('GET', url=get_request_url(f'blocks/{page_id}/children?page_size=100'), headers=headers)
    else:
      response = requests.request('GET', url=get_request_url(f'blocks/{id}/children?page_size=100&start_cursor={start_cursor}'), headers=headers)
    #pprint(response.json())
    res = response.json()
  
    for data in res["results"]:
      try:
        #データベースの場合
        datas["title"] = data["child_database"]["title"]
        datas["id"] = data["id"]
      except:
        #データベースではない場合はスキップ
        continue
      list.append(datas)
      datas = {}
  
    time.sleep(0.3)
    if not res["has_more"]:
      break
    else:
      start_cursor = res["next_cursor"]

  return list


def getdatabase(page_id=None):
  list = []
  datas = {}
  start_cursor = None
  create_json = {}
  
  while True:
    if start_cursor is None:
      response = requests.request('post', url=get_request_url(f'databases/{page_id}/query'), headers=headers,json=create_json,data=json.dumps({'page_size': 100}))
    else:
      response = requests.request('post', url=get_request_url(f'databases/{page_id}/query'), headers=headers,json=create_json,data=json.dumps({'page_size': 100, 'start_cursor': start_cursor}))
    #pprint(response.json())
    res = response.json()
  
    for data in res["results"]:
      try:
        #データベースの場合
        datas["title"] = data["properties"]["ページタイトル"]["title"][0]["plain_text"]
        datas["id"] = data["id"]
      except:
        #データベースではない場合はスキップ
        continue
      list.append(datas)
      datas = {}
  
    time.sleep(0.3)
    if not res["has_more"]:
      break
    else:
      start_cursor = res["next_cursor"]

  return list
