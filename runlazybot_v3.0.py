# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import os
import sys
import botsetting
import requests
import re
import json
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from bs4 import BeautifulSoup

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = botsetting.LINE_CHANNEL_SECRET
channel_access_token = botsetting.LINE_CHANNEL_ACCESS_TOKEN
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)
filter_softjob = ["[情報]", "[公告]"]
filter_default = [
    ["default", "[公告]", "[發錢]"]
]
filter_test = [
    ["soft_job", "[情報]"],
    ["lol"],
    ["nba", "[live]"],
    ["beauty"],
    ["baseball"]
]
filter_formal = []
i = 0
for filter_clns in filter_test:
    # print(filter_clns)    
    # #if filter_clns[0] not in ["default"]:
    # filter_clns.extend(filter_default[0][1:])
    # print("....filter 1....")
    # print(filter_clns)
    # filter_formal.extend(filter_clns)
    # print(".......filter 2 ........")
    # print(filter_formal)
    filter_test[i].extend(filter_default[0][1:])
    i += 1
print("...........FULL FILTER............")
print(filter_test)
@app.route("/callback", methods=['POST'])

def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

#     if event is MessageEvent and message is TextMessage, then echo text
#    for event in events:
#        if not isinstance(event, MessageEvent):
#            continue
#        if not isinstance(event.message, TextMessage):
#            continue
#
#        line_bot_api.reply_message(
#            event.reply_token,
#            TextSendMessage(text="U just said: " + event.message.text)
#        )

    all_template_message = TemplateSendMessage()
    carousel_template_message = TemplateSendMessage()
    simple_board_name = ""
    simple_push_rate = 90
    filter_simple = []
    for event in events:
        if isinstance(event, MessageEvent):
            # if event.message.text.lower() == 'lazybot' or event.message.text.lower() == "lazynoob":
            if event.message.text.lower() in ["lazybot", "lazbot", "lzbot", "lazynoob", "lazyn00b"]:
                all_template_message = TemplateSendMessage(
                    alt_text = '安安 \n\n指令說明請輸入\"LzHelp\"(大小寫皆可)',
                    template = ButtonsTemplate(
                        thumbnail_image_url = "https://farm1.staticflickr.com/369/30705578944_b898fa0458_h.jpg",
                        title = '安安',
                        text = '請選擇下列服務',
                        actions = [
                            MessageTemplateAction(
                                label = 'PTT表特版五大熱門文章',
                                text = 'BEAU'
                            ),
                            MessageTemplateAction(
                                label = '其他指令說明',
                                text = 'LzHelp'
                            ),
                            URITemplateAction(
                                label = "借你看冰島相簿喔(flickr)",
                                uri = "https://www.flickr.com/photos/132023410@N06/albums/72157673424430564"
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(
                event.reply_token,
                all_template_message
                )

            if event.message.text.lower() in ["lzhelp", "lazhelp", "lazyhelp"]:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text= \
                    "指令說明\n" + \
                    "(😃 所有指令大小寫皆可)\n\n" + \
                    "❤[+]Beauty版熱文\n" + \
                    "(手機觀看可得較佳效果)\n" + \
                    "❇Beau\n\n" + \
                    "❤[+]查看PTT各版熱門文章\n" + \
                    "(推文數可不輸入，預設50)\n" + \
                    "❇LzPtt (空格) 版名 (空格) 推文數標準\n" + \
                    "以下為範例: \n" + \
                    "❇LzPtt car\n" + \
                    "❇LzPtt nba 80\n" + \
                    "❇LzPtt gossiping 10\n\n" + \
                    "❤[+]利用關鍵字搜尋PTT看板文章\n" + \
                    "(推文數可不輸入，預設50)\n" + \
                    "❇LzPttS (空格) 版名 (空格) 搜尋關鍵字 (空格) 推文數標準\n" + \
                    "以下為範例: \n" + \
                    "❇LzPttS car 心得\n" + \
                    "❇LzPttS nba live 30\n" + \
                    "❇LzPttS movie 好雷 10\n")
                )

            # if event.message.text.lower() == '表特':
            #     all_template_message = PttBeauty()
            #     line_bot_api.reply_message(
            #     event.reply_token,
            #     TextSendMessage(text=all_template_message)
            #     )

            # if event.message.text.lower() == 'nba':
            #     all_template_message = PttNBA()
            #     line_bot_api.reply_message(
            #     event.reply_token,
            #     TextSendMessage(text=all_template_message)
            #     )

            # if event.message.text.lower() == 'nbafilm':
            #     all_template_message = PttNBAFilm()
            #     line_bot_api.reply_message(
            #     event.reply_token,
            #     TextSendMessage(text=all_template_message)
            #     )

            # if event.message.text.lower() == 'softjob':
            #     simple_board_name = "Soft_Job"
            #     simple_push_rate = 20
            #     filter_simple = filter_softjob
            #     all_template_message = ptt_simple_board(simple_board_name, simple_push_rate, filter_simple)
            #     line_bot_api.reply_message(
            #     event.reply_token,
            #     TextSendMessage(text=all_template_message)
            #     )

            if event.message.text.lower().startswith("lzptt "):
                #print(event.message.text)
                simple_board_name_input = re.split("\s*", event.message.text)
                #print(simple_board_name_input)
                simple_board_name = simple_board_name_input[1]
                #print("..............<<" + simple_board_name)
                #吃輸入的推文數
                try:
                    simple_push_rate = int(simple_board_name_input[2])
                except:
                    #print("........input push rate fail1")
                    simple_push_rate = 50
                print("........push_rate_1" + str(simple_push_rate))
                for filter_ctr in filter_test:
                    if simple_board_name == filter_ctr[0]:
                        filter_simple = filter_ctr[1:]
                if not filter_simple:
                    filter_simple = filter_default[0][1:]
                    #print(filter_simple)
                #設定filter，1 = 標題黑名單filter(內建)，2 = 標題白名單filter(user輸入)
                simple_filter_type = 1
                all_template_message = ptt_simple_board(simple_board_name, simple_push_rate, filter_simple, simple_filter_type)
                #print(all_template_message)
                print(len(all_template_message))
                if not all_template_message:
                    all_template_message = \
                    "請降低推文數標準，設定方式可參考LzPtt指令說明: \n\n" + \
                    "LzPtt (空格) PTT版名 (空格) 推文數標準\n\n" + \
                    "例: LzPtt NBA 70\n\n" + \
                    "或使用指令\"LzHelp\"了解詳細資訊\n"
                if len(all_template_message) >= 2000:
                    all_template_message = \
                    "文章過多，請提高推文數。\n\n" + \
                    "LzPtt (空格) PTT版名 (空格) 推文數標準\n" + \
                    "例: lzPtt NBA 70\n\n" + \
                    "或使用指令\"LzHelp\"了解詳細資訊\n"
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=all_template_message)
                )

            if event.message.text.lower().startswith("lzptts "):
                print(event.message.text)
                simple_board_name_input = re.split("\s*", event.message.text)
                #print(simple_board_name_input)
                simple_board_name = simple_board_name_input[1]
                #print("..............<<" + simple_board_name)
                try:
                    filter_simple = simple_board_name_input[2]
                    bypass_proc = 0
                except:
                    all_template_message = \
                    "請輸入關鍵字以供搜尋，設定方式可參考LzPttS指令說明: \n\n" + \
                    "LzPttS (空格) PTT版名 (空格) 搜尋關鍵字 (空格) 推文數標準\n\n" + \
                    "例: LzPttS car 心得\n" + \
                    "例: LzPttS NBA box 70\n" + \
                    "或使用指令\"LzHelp\"了解詳細資訊\n"
                    bypass_proc = 1
                if bypass_proc == 0:
                    #吃輸入的推文數
                    try:
                        simple_push_rate = int(simple_board_name_input[3])
                    except:
                        #print("........input push rate fail1")
                        simple_push_rate = 50
                    print("........push_rate_1" + str(simple_push_rate))
                    simple_filter_type = 2
                    all_template_message = ptt_simple_board(simple_board_name, simple_push_rate, filter_simple, simple_filter_type)
                    #print(all_template_message)
                    print(len(all_template_message))
                    if not all_template_message:
                        if search_match <=0:
                            all_template_message = \
                            "查無結果，請調整搜尋關鍵字，LzPtts指令說明: \n\n" + \
                            "LzPtts (空格) PTT版名 (空格) 搜尋關鍵字 (空格) 推文數標準\n\n" + \
                            "例: LzPtts car 心得\n" + \
                            "例: LzPtts nba box 70\n"
                        elif push_rate_match <= 0:
                            all_template_message = \
                            "請降低推文數標準，LzPtts指令說明: \n\n" + \
                            "LzPtts (空格) PTT版名 (空格) 搜尋關鍵字 (空格) 推文數標準\n\n" + \
                            "例: LzPtts car 心得\n" + \
                            "例: LzPtts nba box 70\n"
                    if len(all_template_message) >= 2000:
                        all_template_message = \
                        "文章過多，請調整設定，LzPtts指令說明: 。\n\n" + \
                        "LzPtts (空格) PTT版名 (空格) 搜尋關鍵字 (空格) 推文數標準\n\n" + \
                        "例: LzPtts car 心得\n" + \
                        "例: LzPtts nba box 70\n"
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=all_template_message)
                )

            if event.message.text.lower() == 'beau':
                all_template_message = ''
                article_list_sorted = PttBeautyCarousel()
                print(article_list_sorted)
                all_template_message = TemplateSendMessage(
                    #PC版不支援CarouselTemplate，只會顯示這段訊息，手機板剛好不會顯示，拿來當PC版的資訊欄位
                    alt_text = "PTT表特版近日推文數前5名\n\n" + "(" + str(article_list_sorted[0][0]) + "推) " \
                     + article_list_sorted[0][2] + "\n" + article_list_sorted[0][1] \
                     + "\n\n" + "(" + str(article_list_sorted[1][0]) + "推) " \
                     + article_list_sorted[1][2] + "\n" + article_list_sorted[1][1] \
                     + "\n\n" + "(" + str(article_list_sorted[2][0]) + "推) " \
                     + article_list_sorted[2][2] + "\n" + article_list_sorted[2][1] \
                     + "\n\n" + "(" + str(article_list_sorted[3][0]) + "推) " \
                     + article_list_sorted[3][2] + "\n" + article_list_sorted[3][1] \
                     + "\n\n" + "(" + str(article_list_sorted[4][0]) + "推) " \
                     + article_list_sorted[4][2] + "\n" + article_list_sorted[4][1] \
                     ,
                    template = CarouselTemplate(
                        columns = [
                            CarouselColumn(
                                thumbnail_image_url = article_list_sorted[0][3],
                                #反正CarouselTemplate的title欄位非必要，放了也沒比較好看，就省掉
                                #title = "( " + str(article_list_sorted[0][0]) + "推 )",
                                text = "( " + str(article_list_sorted[0][0]) + "推 ) " + article_list_sorted[0][2],
                                actions = [
                                    URITemplateAction(
                                        label = "PTT原文連結",
                                        uri = article_list_sorted[0][1]
                                    )
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url = article_list_sorted[1][3],
                                #title = "( " + str(article_list_sorted[1][0]) + "推 ) ",
                                text = "( " + str(article_list_sorted[1][0]) + "推 ) " + article_list_sorted[1][2],
                                actions = [
                                    URITemplateAction(
                                        label = "PTT原文連結",
                                        uri = article_list_sorted[1][1]
                                    )
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url = article_list_sorted[2][3],
                                #title = "( " + str(article_list_sorted[2][0]) + "推 )",
                                text = "( " + str(article_list_sorted[2][0]) + "推 ) " + article_list_sorted[2][2],
                                actions = [
                                    URITemplateAction(
                                        label = "PTT原文連結",
                                        uri = article_list_sorted[2][1]
                                    )
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url = article_list_sorted[3][3],
                                #title = "( " + str(article_list_sorted[3][0]) + "推 )",
                                text = "( " + str(article_list_sorted[3][0]) + "推 ) " + article_list_sorted[3][2],
                                actions = [
                                    URITemplateAction(
                                        label = "PTT原文連結",
                                        uri = article_list_sorted[3][1]
                                    )
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url = article_list_sorted[4][3],
                                #title = "( " + str(article_list_sorted[4][0]) + " 推)",
                                text = "( " + str(article_list_sorted[4][0]) + " 推) " + article_list_sorted[4][2],
                                actions = [
                                    URITemplateAction(
                                        label = "PTT原文連結",
                                        uri = article_list_sorted[4][1]
                                    )
                                ]
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(
                event.reply_token,
                all_template_message
                )
                #用完把list內容刪掉，達到重置的效果，不然舊的紀錄還在，結果累積推文數最高的那篇
            # article_list = []
            # article_list_sorted = []
            del all_template_message
            del article_list[:]
            del article_list_sorted[:]
            simple_board_name = ""
            simple_push_rate is None
            del filter_simple[:]

    return 'OK'
article_list = []
push_rate_match = 0
search_match = 0
push_rate_peak = 0

def crawPageBeauty(url, push_rate, soup):
    #r-ent是每頁裡面各篇文的class
    for r_ent in soup.find_all(class_="r-ent"):
        try:
            #抓各篇文章uri的後半段
            link = r_ent.find('a')['href']
            if 'M.1430099938.A.3B7' in link:
                continue
            comment_rate = ""
            if (link):
                #文章uri存在的話，表示沒被刪文，可以繼續抓值(標題、推文數)，因為link的網址只有後半段，自己接起來
                title = r_ent.find(class_="title").text.strip()
                rate = r_ent.find(class_="nrec").text
                URL = 'https://www.ptt.cc' + link
                #print("........" + URL)
                if (rate):
                    comment_rate = rate
                    if rate.find(u'爆') > -1:
                        comment_rate = 100
                    if rate.find('X') > -1:
                        comment_rate = -1 * int(rate[1])
                else:
                    comment_rate = 0
                #只看推文數 >= push_rate設定的
                if int(comment_rate) >= push_rate:
                    #print("        HighPost: " + URL)
                    #抓URL網頁內容給res_post
                    res_post = requests.get(URL, verify=False)
                    #把網頁內容parser過後丟給soup_post
                    soup_post = BeautifulSoup(res_post.text, "lxml")
                    #比較像暫時解，因為我抓全部<a >但前5個會是PTT的連結，後面才開始是po文內的，就設定個起始值降loading
                    img_uri_num = 5
                    img_links_list = []
                    #沒打算抓很多連結來分析，只要有一張圖就可以了，讓他抓第5到10個連結
                    for img_uri_num in range(img_uri_num, 10, +1):
                        #print(img_uri_num)
                        img_links = soup_post.select("a")[img_uri_num]["href"]
                        #print(img_links)
                        #如果該連結結尾是.jpg，那就可以用
                        if img_links.lower().endswith(".jpg"):
                            #如果是https就OK，不是的話要把http換成https，LINE不支援http的圖
                            if not img_links.startswith("https://"):
                                img_links = re.sub("http", "https", img_links)
                                #print(img_links)
                            #雖然只要一張，但抓都抓了，存個5張先，可能後面有用
                            img_links_list.append(img_links)
                        #非.jpg結尾的，如果是imgur圖床的，幫他加個
                        elif "imgur" in img_links:
                            img_links = img_links + ".jpg"
                            print(img_links)
                            if not img_links.startswith("https://"):
                                img_links = re.sub("http", "https", img_links)
                                #print(img_links)
                            #雖然只要一張，但抓都抓了，有幾張存幾張，可能後面有用
                            img_links_list.append(img_links)
                    #一篇文的資料抓完了，存進list
                    article_list.append((int(comment_rate), URL, title, img_links_list[0]))                
        except:
            # print u'crawPage function error:',r_ent.find(class_="title").text.strip()
            # print('本文已被刪除')
            print('delete')

def simple_craw_page(url, push_rate, soup, filter_simple, simple_filter_type):
    #r-ent是每頁裡面各篇文的class
    #print(filter_softjob)
    global push_rate_match
    global search_match
    global push_rate_peak
    for r_ent in soup.find_all(class_="r-ent"):
        try:
            #抓各篇文章uri的後半段
            link = r_ent.find('a')['href']
            # if 'M.1430099938.A.3B7' in link:
            #     continue
            comment_rate = ""
            if (link):
                #文章uri存在的話，表示沒被刪文，可以繼續抓值(標題、推文數)，因為link的網址只有後半段，自己接起來
                title = r_ent.find(class_="title").text.strip()
                rate = r_ent.find(class_="nrec").text
                URL = 'https://www.ptt.cc' + link
                #print("........" + URL)
                if (rate):
                    comment_rate = rate
                    if rate.find(u'爆') > -1:
                        comment_rate = 100
                    if rate.find('X') > -1:
                        comment_rate = -1 * int(rate[1])
                else:
                    comment_rate = 0
                #只看推文數 >= push_rate設定的，同時依標題分類黑名單過濾
                if simple_filter_type == 1:                    
                    if int(comment_rate) >= push_rate and not (title.lower().startswith(tuple(filter_simple))):
                        article_list.append((int(comment_rate), URL, title))
                        #print(article_list)
                    elif not title.lower().startswith(tuple(filter_simple)):
                        push_rate_peak = int(comment_rate)
                        print("............push peak: " + comment_rate)
                elif simple_filter_type == 2:
                    print(str(comment_rate) + "   keyword   " + filter_simple.lower() + "  >?  " + title.lower() + "\n\n")
                    # print(filter_simple.encode("UTF-8"))
                    # print("\n")
                    # print(title.encode("UTF-8"))
                    if int(comment_rate) >= push_rate and (filter_simple.lower() in title.lower()):
                        article_list.append((int(comment_rate), URL, title))
                        push_rate_match += 1
                        print("......push status is : " + str(push_rate_match))
                        # print(article_list)                    
        except:
            # print u'crawPage function error:',r_ent.find(class_="title").text.strip()
            # print('本文已被刪除')
            print('delete')
    #print(article_list)

# def crawPageNBA(url, push_rate, soup):
#     #r-ent是每頁裡面各篇文的class
#     for r_ent in soup.find_all(class_="r-ent"):
#         try:
#             #抓各篇文章uri的後半段
#             link = r_ent.find('a')['href']
#             # if 'M.1430099938.A.3B7' in link:
#             #     continue
#             comment_rate = ""
#             if (link):
#                 #文章uri存在的話，表示沒被刪文，可以繼續抓值(標題、推文數)，因為link的網址只有後半段，自己接起來
#                 title = r_ent.find(class_="title").text.strip()
#                 rate = r_ent.find(class_="nrec").text
#                 URL = 'https://www.ptt.cc' + link
#                 #print("........" + URL)
#                 if (rate):
#                     comment_rate = rate
#                     if rate.find(u'爆') > -1:
#                         comment_rate = 100
#                     if rate.find('X') > -1:
#                         comment_rate = -1 * int(rate[1])
#                 else:
#                     comment_rate = 0
#                 #只看推文數 >= push_rate設定的
#                 #print("................" + str(comment_rate) + title)
#                 if int(comment_rate) >= push_rate and not re.search("[live]", title, re.IGNORECASE) and not re.search("[公告]", title):
#                 #if int(comment_rate) >= push_rate:
#                     #print(comment_rate + title)
#                     article_list.append((int(comment_rate), URL, title))                
#         except:
#             # print u'crawPage function error:',r_ent.find(class_="title").text.strip()
#             # print('本文已被刪除')
#             print('delete')

# def PttBeauty():
#     TargetURI = "https://www.ptt.cc/bbs/Beauty/index.html"
#     res = requests.get(TargetURI, verify=False)
#     #print(res.text)
#     #ResContent = res.text
#     soup = BeautifulSoup(res.text, "lxml")
#     #print("    soup>>>" + soup.prettify())
#     #class=btn wide
#     LatestPageURI = soup.select('.btn.wide')[1]['href']
#     #print("    URI>>> " + LatestPageURI)
#     LatestPageNum = re.match('/bbs/Beauty/index(.*).html',LatestPageURI)
#     #print("    PageNum>>> " + LatestPageNum.group(1))
#     LPN = int(LatestPageNum.group(1)) + 1
#     push_rate = 30  # 推文
#     page_uri_list = []
#     for page in range(LPN, LPN-3, -1):
#         page_uri = "https://www.ptt.cc/bbs/Beauty/index" + str(page) + ".html"
#         page_uri_list.append(page_uri)
#     #print("    PageURI>>> " + page_uri)
#     #print(page_uri_list)
#     while page_uri_list:
#         index = page_uri_list.pop(0)
#         #print("    try to parse: " + index)
#         res = requests.get(index, verify=False)
#         soup = BeautifulSoup(res.text, 'lxml')
#         # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
#         if (soup.title.text.find('Service Temporarily') > -1):
#             page_uri_list.append(index)
#             # print u'error_URL:',index
#             # time.sleep(1)
#         else:
#             crawPageBeauty(index, push_rate, soup)
#             # print u'OK_URL:', index
#             # time.sleep(0.05)
#     article_list_sorted = []
#     article_list_sorted = sorted(article_list, key = lambda x:x[0], reverse = True)
#     #print(article_list_sorted)
#     all_template_message = ''
#     for article in article_list_sorted:
#         data = "(" + str(article[0]) + "推) " + article[2] + "\n" + article[1] + "\n" + article[3] + "\n\n"
#         all_template_message += data
#     return all_template_message

def PttBeautyCarousel():
    TargetURI = "https://www.ptt.cc/bbs/Beauty/index.html"
    res = requests.get(TargetURI, verify=False)
    #print(res.text)
    #ResContent = res.text
    soup = BeautifulSoup(res.text, "lxml")
    #print("    soup>>>" + soup.prettify())
    #爬最新-1頁面連結(因為直接get的話，第1頁是index.html)
    LatestPageURI = soup.select('.btn.wide')[1]['href']
    #print("    URI>>> " + LatestPageURI)
    #從連結抓出最新-1頁數
    LatestPageNum = re.match('/bbs/Beauty/index(.*).html',LatestPageURI)
    #print("    PageNum>>> " + LatestPageNum.group(1))
    #最新頁雖然是index.html，但剛剛的數字+1也能連的到，所以+1來用
    LPN = int(LatestPageNum.group(1)) + 1
    #設個閥值，想降些loading，這支parser好像不太快
    push_rate = 20  # 推文
    page_uri_list = []
    #抓個3頁差不多吧，表特版文章更新不算快，把這三頁的uri接好存到page_uri_list
    for page in range(LPN, LPN-3, -1):
        page_uri = "https://www.ptt.cc/bbs/Beauty/index" + str(page) + ".html"
        page_uri_list.append(page_uri)
    #print("    PageURI>>> " + page_uri)
    #print(page_uri_list)
    while page_uri_list:
        index = page_uri_list.pop(0)
        #print("    try to parse: " + index)
        #爬頁面內容出來
        res = requests.get(index, verify=False)
        soup = BeautifulSoup(res.text, 'lxml')
        #如網頁忙線中,則先將網頁加入page_uri_list等1秒後重試
        if (soup.title.text.find('Service Temporarily') > -1):
            page_uri_list.append(index)
            # print u'error_URL:',index
            # time.sleep(1)
        else:
            crawPageBeauty(index, push_rate, soup)
            # print u'OK_URL:', index
            # time.sleep(0.05)
    article_list_sorted = []
    article_list_sorted = sorted(article_list, key = lambda x:x[0], reverse = True)
    #print(article_list_sorted)    
    # for article in article_list_sorted:
    #     data = "(" + str(article_list_sorted[0]) + "推) " + article_list_sorted[2] + "\n" + article_list_sorted[1] + "\n" + article_list_sorted[3] + "\n\n"
    #     all_template_message += data
    return article_list_sorted

def ptt_simple_board(simple_board_name, simple_push_rate, filter_simple, simple_filter_type):
    global search_match
    global push_rate_match
    global push_rate_peak
    search_match = 0
    push_rate_match = 0
    push_rate_peak = 0
    #吃傳進來的板名(simple_board_name)
    TargetURI = "https://www.ptt.cc/bbs/" + simple_board_name + "/index.html"
    rs = requests.session()
    if simple_board_name in ["gossiping", "sex"]:
        #print("........start to verify 18+")
        adult_payload = {
        "from" : "/bbs/" + simple_board_name + "/index.html",
        "yes" : "yes"
        }
        res = rs.post("https://www.ptt.cc/ask/over18", verify=False, data = adult_payload)
        #print(res.text)

    res = rs.get(TargetURI, verify=False)
    #print(res.text)
    #ResContent = res.text
    soup = BeautifulSoup(res.text, "lxml")
    #print("    soup>>>" + soup.prettify())
    #class=btn wide
    #抓最新-1頁連結
    try:
        LatestPageURI = soup.select('.btn.wide')[1]['href']
    except:
        all_template_message = "發生錯誤，可至PTT確認版名。\n https://www.ptt.cc/hotboard.html"
        return all_template_message
    #print("    URI>>> " + LatestPageURI)
    #從連接拆出最新-1頁數
    noindex_page_uri = re.split("index", LatestPageURI)
    #print(noindex_page_uri)
    #print(noindex_page_uri[1][0:-5])
    LatestPageNum = noindex_page_uri[1][0:-5]
    #print( LatestPageNum )
    #print(LatestPageNum.group(1))
    LPN = int(LatestPageNum) + 1
    #吃傳進來的推文閥值
    push_rate = simple_push_rate
    print("....push_erate = simple..." + str(push_rate))
    page_uri_list = []
    #抓3頁，把uri接起來存在page_uri_list
    for page in range(LPN, LPN-3, -1):
        page_uri = "https://www.ptt.cc/bbs/" + simple_board_name + "/index" + str(page) + ".html"
        page_uri_list.append(page_uri)
    #print("    PageURI>>> " + page_uri)
    #print(page_uri_list)
    while page_uri_list:
        index = page_uri_list.pop(0)
        #print("    try to parse: " + index)

        res = rs.get(index, verify=False)
        soup = BeautifulSoup(res.text, 'lxml')
        #如網頁忙線中,則先將網頁加入page_uri_list等1秒重試
        if (soup.title.text.find('Service Temporarily') > -1):
            page_uri_list.append(index)
            # print u'error_URL:',index
            # time.sleep(1)
        else:
            simple_craw_page(index, push_rate, soup, filter_simple, simple_filter_type)
            # print u'OK_URL:', index
            # time.sleep(0.05)
    #print(article_list)
    article_list_sorted = []
    article_list_sorted = sorted(article_list, key = lambda x:x[0], reverse = True)
    #print(article_list_sorted)
    all_template_message = ''
    for article in article_list_sorted:
        data = "(" + str(article[0]) + "推) " + article[2] + "\n" + article[1] + "\n\n"
        all_template_message += data
    return all_template_message

# def PttNBA():
#     TargetURI = "https://www.ptt.cc/bbs/NBA/index.html"
#     res = requests.get(TargetURI, verify=False)
#     #print(res.text)
#     #ResContent = res.text
#     soup = BeautifulSoup(res.text, "lxml")
#     #print("    soup>>>" + soup.prettify())
#     #class=btn wide
#     #抓最新-1頁的連結
#     LatestPageURI = soup.select('.btn.wide')[1]['href']
#     #print("    URI>>> " + LatestPageURI)
#     #從連接拆出最新-1頁數
#     LatestPageNum = re.match('/bbs/NBA/index(.*).html',LatestPageURI)
#     #print("    PageNum>>> " + LatestPageNum.group(1))
#     LPN = int(LatestPageNum.group(1)) + 1
#     #設定推文數閥值
#     push_rate = 50
#     page_uri_list = []
#     for page in range(LPN, LPN-3, -1):
#         page_uri = "https://www.ptt.cc/bbs/NBA/index" + str(page) + ".html"
#         page_uri_list.append(page_uri)
#     #print("    PageURI>>> " + page_uri)
#     #print(page_uri_list)
#     while page_uri_list:
#         index = page_uri_list.pop(0)
#         #print("    try to parse: " + index)
#         res = requests.get(index, verify=False)
#         soup = BeautifulSoup(res.text, 'lxml')
#         #如網頁忙線中,則先將網頁加入page_uri_list等1秒重試
#         if (soup.title.text.find('Service Temporarily') > -1):
#             page_uri_list.append(index)
#             # print u'error_URL:',index
#             # time.sleep(1)
#         else:
#             crawPageNBA(index, push_rate, soup)
#             # print u'OK_URL:', index
#             # time.sleep(0.05)
#     article_list_sorted = []
#     article_list_sorted = sorted(article_list, key = lambda x:x[0], reverse = True)
#     #print(article_list_sorted)
#     all_template_message = ''
#     for article in article_list_sorted:
#         data = "(" + str(article[0]) + "推) " + article[2] + "\n" + article[1] + "\n\n"
#         all_template_message += data
#     return all_template_message

# def PttNBAFilm():
#     TargetURI = "https://www.ptt.cc/bbs/NBA_Film/index.html"
#     res = requests.get(TargetURI, verify=False)
#     #print(res.text)
#     #ResContent = res.text
#     soup = BeautifulSoup(res.text, "lxml")
#     #print("    soup>>>" + soup.prettify())
#     #class=btn wide
#     #抓最新-1頁的連結
#     LatestPageURI = soup.select('.btn.wide')[1]['href']
#     #print("    URI>>> " + LatestPageURI)
#     #從連接拆出最新-1頁數
#     LatestPageNum = re.match('/bbs/NBA_Film/index(.*).html',LatestPageURI)
#     #print("    PageNum>>> " + LatestPageNum.group(1))
#     LPN = int(LatestPageNum.group(1)) + 1
#     #設定推文數閥值
#     push_rate = 20
#     page_uri_list = []
#     for page in range(LPN, LPN-3, -1):
#         page_uri = "https://www.ptt.cc/bbs/NBA_Film/index" + str(page) + ".html"
#         page_uri_list.append(page_uri)
#     #print("    PageURI>>> " + page_uri)
#     #print(page_uri_list)
#     while page_uri_list:
#         index = page_uri_list.pop(0)
#         #print("    try to parse: " + index)
#         res = requests.get(index, verify=False)
#         soup = BeautifulSoup(res.text, 'lxml')
#         #如網頁忙線中,則先將網頁加入page_uri_list等1秒重試
#         if (soup.title.text.find('Service Temporarily') > -1):
#             page_uri_list.append(index)
#             # print u'error_URL:',index
#             # time.sleep(1)
#         else:
#             crawPageNBA(index, push_rate, soup)
#             # print u'OK_URL:', index
#             # time.sleep(0.05)
#     article_list_sorted = []
#     article_list_sorted = sorted(article_list, key = lambda x:x[0], reverse = True)
#     #print(article_list_sorted)
#     all_template_message = ''
#     for article in article_list_sorted:
#         data = "(" + str(article[0]) + "推) " + article[2] + "\n" + article[1] + "\n\n"
#         all_template_message += data
#     return all_template_message


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)