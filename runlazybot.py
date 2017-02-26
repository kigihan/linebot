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

    all_template_message = TemplateSendMessage()
    for event in events:
        if isinstance(event, MessageEvent):
            if event.message.text.lower() == 'bmenu':
                all_template_message = TemplateSendMessage(
                    alt_text = 'AltText',
                    template = ButtonsTemplate(
                        thumbnail_image_url = 'https://farm1.staticflickr.com/369/30705578944_b898fa0458_h.jpg/200',
                        title = 'menutitle',
                        text = 'here is text',
                        actions = [
                            MessageTemplateAction(
                                label = 'bt1_label',
                                text = 'bt1_twxt'
                            ),
                            MessageTemplateAction(
                                label = 'bt2_label',
                                text = 'bt2_twxt'
                            ),
                            MessageTemplateAction(
                                label = 'bt3_label',
                                text = 'bt3_twxt'
                            )
                        ]
                    )
                )
            # if event.message.text.lower() == 'bmenu 表特':
            #     all_template_message = TemplateSendMessage(
            #         alt_text = 'alttexthere',
            #         template = CarouselTemplate(
            #             columns = [
            #                 CarouselColumn(
            #                     thumbnail_image_url = 'https://farm1.staticflickr.com/369/30705578944_b898fa0458_h.jpg/200',
            #                     title = 'pic 1 meow',
            #                     text = 'a lazy cat behind window',
            #                     actions = [
            #                         URITemplateAction(
            #                             label = 'link here',
            #                             uri = 'https://farm1.staticflickr.com/369/30705578944_b898fa0458_h.jpg/200'
            #                         )
            #                     ]
            #                 )
            #             ]
            #         )
            #     )
            
            if event.message.text.lower() == 'bmenu 表特':
                all_template_message = PttBeauty()

            line_bot_api.reply_message(
                event.reply_token,
#                TextSendMessage(text="U just said: " + event.message.text)
                all_template_message
            )

    return 'OK'

def PttBeauty():
    TargetURI = "https://www.ptt.cc/bbs/Beauty/index.html"
    res = requests.get(TargetURI)
    #print(res.text)
    #ResContent = res.text
    soup = BeautifulSoup(res.text, "html.parser")
    #print("    soup>>>" + soup.prettify())
    LatestPageURI = soup.select('.btn.wide')[1]['href']
    #print("    URI>>> " + LatestPageURI)
    LatestPageNum = re.match('/bbs/Beauty/index(.*).html',LatestPageURI)
    print("    PageNum>>> " + LatestPageNum.group(1))
    for page in range(LatestPageNum, LatestPageNum-10, -1):
        page_uri = "https://www.ptt.cc/bbs/Beauty/index" + str(LatestPageNum) + ".html"
        page_uri_list.append(page_uri)
    print("    PageList>>>" + page_uri_list)
    return 'OK'


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
