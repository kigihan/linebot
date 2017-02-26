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

    # if event is MessageEvent and message is TextMessage, then echo text
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
    
    for event in events:
        if isinstance(event, MessageEvent):
            all_template_message = ""
            carousel_template_message = ""
            if event.message.text.lower() == 'bmenu':                
                all_template_message = TemplateSendMessage(
                    alt_text = 'PC敘述',
                    template = ButtonsTemplate(
                        thumbnail_image_url = "https://farm1.staticflickr.com/369/30705578944_b898fa0458_h.jpg",
                        title = '標題',
                        text = '文字敘述',
                        actions = [
                            MessageTemplateAction(
                                label = '訊息標題',
                                text = '訊息1'
                            ),
                            MessageTemplateAction(
                                label = 'bt2_label',
                                text = 'bt2_twxt'
                            ),
                            URITemplateAction(
                                label = "URI標題",
                                uri = "https://farm1.staticflickr.com/369/30705578944_b898fa0458_h.jpg"
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(
                event.reply_token,
                all_template_message
                )

            if event.message.text.lower() == '表特':
                all_template_message = PttBeauty()
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=all_template_message)
                )

            if event.message.text.lower() == 'beau':
                article_list_sorted = ""
                article_list_sorted = PttBeautyCarousel()
                print(article_list_sorted)
                all_template_message = TemplateSendMessage(
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

            # if event.message.text.lower() == 'beau':
            #     #carousel_template_message = ''
            #     #article_list_sorted = PttBeautyCarousel()
            #     #print(article_list_sorted)                
            #     carousel_template_message = TemplateSendMessage(
            #         alt_text = 'PTTtitle',
            #         template = CarouselTemplate(
            #             columns = [
            #                 CarouselColumn(
            #                     thumbnail_image_url = "https://i.imgur.com/gAaUTT6.jpg",
            #                     title = "11111",
            #                     text = "tttttttttttext",
            #                     actions = [
            #                         URITemplateAction(
            #                             label = "LL1",
            #                             uri = "https://www.ptt.cc/bbs/Beauty/M.1488020739.A.2BD.html"
            #                         )
            #                     ]
            #                 ),
            #                 CarouselColumn(
            #                     thumbnail_image_url = "https://i.imgur.com/gAaUTT6.jpg",
            #                     title = "22",
            #                     text = "t2",
            #                     actions = [
            #                         URITemplateAction(
            #                             label = "L2",
            #                             uri = "https://www.ptt.cc/bbs/Beauty/M.1487987174.A.32C.html"
            #                         )
            #                     ]
            #                 )
            #             ]
            #         )
            #     )
            #     print(carousel_template_message)
            #     line_bot_api.reply_message(
            #     event.reply_token,
            #     carousel_template_message
            #     )

    return 'OK'
article_list = []

def crawPage(url, push_rate, soup):
    for r_ent in soup.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']
            if 'M.1430099938.A.3B7' in link:
                continue
            comment_rate = ""
            if (link):
                # 確定得到url再去抓 標題 以及 推文數
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
                # 比對推文數
                if int(comment_rate) >= push_rate:
                    #print("        HighPost: " + URL)
                    res_post = requests.get(URL, verify=False)
                    soup_post = BeautifulSoup(res_post.text, "html.parser")
                    img_uri_num = 5
                    img_links_list = []
                    for img_uri_num in range(img_uri_num, 10, +1):
                        img_links = soup_post.select("a")[img_uri_num]["href"]
                        #print(img_links)
                        if img_links.endswith(".jpg"):
                            if not img_links.startswith("https://"):
                                img_links = re.sub("http", "https", img_links)
                                #print(img_links)
                            img_links_list.append(img_links)
                    # for link in img_links:
                    #     print("    start FOR")
                    #     print(link)
                    #     if re.match(r"^https?://(i.)?(m.)?imgur.com", link["href"]):
                    #         print("    if(re.match): " + link)
                    #         if not link.endswith(".jpg"):
                    #             link += ".jpg"
                    #         img_links_list.append(link["href"])
                    #         print(link)

                    article_list.append((int(comment_rate), URL, title, img_links_list[0]))                
        except:
            # print u'crawPage function error:',r_ent.find(class_="title").text.strip()
            # print('本文已被刪除')
            print('delete')

def crawPageCarousel(url, push_rate, soup):
    for r_ent in soup.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']
            if 'M.1430099938.A.3B7' in link:
                continue
            comment_rate = ""
            if (link):
                # 確定得到url再去抓 標題 以及 推文數
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
                # 比對推文數
                if int(comment_rate) >= 30:
                    print("        HighPost: " + URL)
                    res_post = requests.get(URL, verify=False)
                    soup_post = BeautifulSoup(res_post.text, "html.parser")
                    img_uri_num = 5
                    img_links_list = []
                    for img_uri_num in range(img_uri_num, 10, +1):
                        img_links = soup_post.select("a")[img_uri_num]["href"]
                        print(img_links)
                        if img_links.endswith(".jpg"):
                            img_links_list.append(img_links)
                    # for link in img_links:
                    #     print("    start FOR")
                    #     print(link)
                    #     if re.match(r"^https?://(i.)?(m.)?imgur.com", link["href"]):
                    #         print("    if(re.match): " + link)
                    #         if not link.endswith(".jpg"):
                    #             link += ".jpg"
                    #         img_links_list.append(link["href"])
                    #         print(link)

                    article_list.append((int(comment_rate), URL, title, img_links_list[0]))
        except:
            # print u'crawPage function error:',r_ent.find(class_="title").text.strip()
            # print('本文已被刪除')
            print('delete')

def PttBeauty():
    TargetURI = "https://www.ptt.cc/bbs/Beauty/index.html"
    res = requests.get(TargetURI, verify=False)
    #print(res.text)
    #ResContent = res.text
    soup = BeautifulSoup(res.text, "html.parser")
    #print("    soup>>>" + soup.prettify())
    LatestPageURI = soup.select('.btn.wide')[1]['href']
    #print("    URI>>> " + LatestPageURI)
    LatestPageNum = re.match('/bbs/Beauty/index(.*).html',LatestPageURI)
    #print("    PageNum>>> " + LatestPageNum.group(1))
    LPN = int(LatestPageNum.group(1)) + 1
    push_rate = 50  # 推文
    page_uri_list = []
    for page in range(LPN, LPN-3, -1):
        page_uri = "https://www.ptt.cc/bbs/Beauty/index" + str(page) + ".html"
        page_uri_list.append(page_uri)
    #print("    PageURI>>> " + page_uri)
    #print(page_uri_list)
    while page_uri_list:
        index = page_uri_list.pop(0)
        #print("    try to parse: " + index)
        res = requests.get(index, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if (soup.title.text.find('Service Temporarily') > -1):
            page_uri_list.append(index)
            # print u'error_URL:',index
            # time.sleep(1)
        else:
            crawPage(index, push_rate, soup)
            # print u'OK_URL:', index
            # time.sleep(0.05)
    article_list_sorted = []
    article_list_sorted = sorted(article_list, key = lambda x:x[0], reverse = True)
    #print(article_list_sorted)
    all_template_message = ''
    for article in article_list_sorted:
        data = "(" + str(article[0]) + "推) " + article[2] + "\n" + article[1] + "\n" + article[3] + "\n\n"
        all_template_message += data
    return all_template_message

def PttBeautyCarousel():
    TargetURI = "https://www.ptt.cc/bbs/Beauty/index.html"
    res = requests.get(TargetURI, verify=False)
    #print(res.text)
    #ResContent = res.text
    soup = BeautifulSoup(res.text, "html.parser")
    #print("    soup>>>" + soup.prettify())
    #爬最新頁數
    LatestPageURI = soup.select('.btn.wide')[1]['href']
    #print("    URI>>> " + LatestPageURI)
    LatestPageNum = re.match('/bbs/Beauty/index(.*).html',LatestPageURI)
    #print("    PageNum>>> " + LatestPageNum.group(1))
    LPN = int(LatestPageNum.group(1)) + 1
    push_rate = 50  # 推文
    page_uri_list = []
    for page in range(LPN, LPN-3, -1):
        page_uri = "https://www.ptt.cc/bbs/Beauty/index" + str(page) + ".html"
        page_uri_list.append(page_uri)
    #print("    PageURI>>> " + page_uri)
    #print(page_uri_list)
    while page_uri_list:
        index = page_uri_list.pop(0)
        #print("    try to parse: " + index)
        res = requests.get(index, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if (soup.title.text.find('Service Temporarily') > -1):
            page_uri_list.append(index)
            # print u'error_URL:',index
            # time.sleep(1)
        else:
            crawPage(index, push_rate, soup)
            # print u'OK_URL:', index
            # time.sleep(0.05)
    article_list_sorted = []
    article_list_sorted = sorted(article_list, key = lambda x:x[0], reverse = True)
    #print(article_list_sorted)    
    # for article in article_list_sorted:
    #     data = "(" + str(article_list_sorted[0]) + "推) " + article_list_sorted[2] + "\n" + article_list_sorted[1] + "\n" + article_list_sorted[3] + "\n\n"
    #     all_template_message += data
    return article_list_sorted

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)