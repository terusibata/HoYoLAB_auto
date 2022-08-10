import notion_create
import notion_search
import time
import keep_alive
import datetime
import HoYo_content
import HoYo_body
import HoYo_Topic
import HoYo_Trend

def main():
    id = 'e963c4b2b7f04eeb89b7e24e5dbbfc5e'
    #notionに現在の時間の親ページIDを取得する
    #現在の時間を取得　  
    dt_now = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=9))
      )
    now = {
        "year":dt_now.year,
        "month":dt_now.month,
        "day":dt_now.day,
        "hour":dt_now.hour,
        "minute":dt_now.minute
    }
    #print(now)
    year_pageid = notion_search.search_page(id,f"{now['year']}年のトレンド")
    month_pageid = notion_search.search_database(year_pageid,f"{now['month']}月のトレンド")
    day_pageid = notion_search.search_page(month_pageid,f"{now['month']}月{now['day']}日のトレンド")
    list_pageid = notion_search.search_database(day_pageid,f"{now['hour']}時{now['minute']}分のトレンド")
    print(list_pageid)

    #トレンド15件取得
    HoYo_Trend_data = HoYo_Trend.trends()

    for count,Trend in enumerate(HoYo_Trend_data):
        print(Trend)
        #ヘッダー2を入力
        notion_create.block.heading_2(list_pageid,f"{count+1}位 {Trend['name']}")
        notion_create.block.text(list_pageid,f"投稿数：{Trend['post_num']} メンバー数：{Trend['member_num']} 閲覧数：{Trend['view_num']}")
        notion_create.block.link_text(list_pageid,f"{Trend['name']}をHoYoLABで開く",f"https://www.hoyolab.com/topicDetail/{Trend['id']}?game_id=2")

        #トレンドのトピックデータベース追加
        Topic_database = notion_create.topic_database.database(list_pageid,f"{Trend['name']} トレンド",Trend["cover_img"])
        #トピックのトレンド一覧を取得
        Topic_list = HoYo_Topic.trends(Trend["id"],30)

        for Topic in Topic_list:
            Topic_database_page = notion_create.topic_database.database_page(Topic_database,Topic)
            if Topic_database_page:
                article(Topic_database_page,Topic["post_id"])
                notion_create.block.text(Topic_database_page,"")
                notion_create.block.divider(Topic_database_page)
                notion_create.block.heading_2(Topic_database_page,"コメント")
                comment(Topic_database_page,Topic["post_id"],Topic["title"])
            else:
                print("ページの追加に失敗しました")
                
        #最新のトピックデータベース追加
        Topic_database = notion_create.topic_database.database(list_pageid,f"{Trend['name']} 最新",Trend["cover_img"])
        #トピックのトレンド一覧を取得
        Topic_list = HoYo_Topic.new(Trend["id"],30)

        for Topic in Topic_list:
            Topic_database_page = notion_create.topic_database.database_page(Topic_database,Topic)
            if Topic_database_page:
                article(Topic_database_page,Topic["post_id"])
                notion_create.block.text(Topic_database_page,"")
                notion_create.block.divider(Topic_database_page)
                notion_create.block.heading_2(Topic_database_page,"コメント")
                comment(Topic_database_page,Topic["post_id"],Topic["title"])
            else:
                print("ページの追加に失敗しました")
                
        notion_create.block.text(list_pageid,"")
        notion_create.block.divider(list_pageid)
        
        

def article(page_id,post_id):
    article_data = HoYo_body.body(post_id)
    if article_data["view_type"] == 1:
        for list in article_data["body"]:
            if list["type"] == "image":
                notion_create.block.image(page_id,list["link"])
            elif list["type"] == "emoticon":
                notion_create.block.image(page_id,list["link"])
            elif list["type"] == "video":
                notion_create.block.Video(page_id,list["link"])
            elif list["type"] == "divider":
                notion_create.block.divider(page_id)
            elif list["type"] == "link":
                notion_create.block.link_text(page_id,list["content"],list["link"])
            elif list["type"] == "text":
                notion_create.block.text(page_id,list["content"])
            elif list["type"] == "vote":
                notion_create.block.divider(page_id)
                notion_create.block.text(page_id,"〘 アンケートフォーム 〙")
                notion_create.block.heading_2(page_id,list["content"]["title"])
                for option in list["content"]["option"]:
                    notion_create.block.text(page_id,option)
                notion_create.block.text(page_id,"")
                notion_create.block.divider(page_id)
            else:
                print("非対応ブロックです")
    elif article_data["view_type"] == 2:
        notion_create.block.text(page_id,article_data["body"]["describe"])
        for img in article_data["body"]["imgs"]:
            notion_create.block.image(page_id,img)
    elif article_data["view_type"] == 5:
        notion_create.block.Video(page_id,article_data["body"]["video"])
        notion_create.block.text(page_id,article_data["body"]["describe"])
    elif article_data["view_type"] == 6:
        notion_create.block.text(page_id,article_data["body"]["topic_content"])
        try:
            notion_create.block.image(page_id,article_data["body"]["cover"])
        except:
            notion_create.block.image(page_id,article_data["body"]["img"])
    else:
        print("view_typeが対応していません")


def comment(page_id,post_id,title):
    comment_page = notion_create.comment_database.database(page_id,"「"+title+"」のコメント")
    comment_data = HoYo_content.comment(post_id)

    for comment in comment_data:
        notion_create.comment_database.database_page(comment_page,comment)

    
keep_alive.keep_alive()

while True:
  try:
    main()
    print("一周完了しました。繰り返します")
  except:
    print("エラーが発生しました")
    time.sleep(5)