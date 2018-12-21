# -*- coding: utf-8 -*-
import json
import os
import calculate
import crawling
import multiprocessing as mp

from threading import Thread
from slackclient import SlackClient
from flask import Flask, request, make_response

app = Flask(__name__)

with open('data/slackBasicInfomation.json', 'rt', encoding='UTF8') as file:
    slack_basic_info = json.load(file)
sc = SlackClient(slack_basic_info['slack_token'])

# threading function
def processing_event(queue):
  while True:
      # 큐가 비어있지 않은 경우 로직 실행
      if not queue.empty():
          slack_event = queue.get()

          # Your Processing Code Block gose to here
          channel = slack_event["event"]["channel"]
          text = slack_event["event"]["text"]

          # 챗봇 크롤링 프로세스 로직 함수
          crawling.crawling_data_all()

          # 아래에 슬랙 클라이언트 api를 호출하세요
          sc.api_call(
              "chat.postMessage",
              channel=channel,
              text=calculate.bot_dialog(text, calculate.analysis_text(text)),
          )
          
# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):

  if event_type == "app_mention":
      event_queue.put(slack_event)
      return make_response("App mention message has been sent", 200, )

@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"
                                                            })

    if slack_basic_info['slack_verification'] != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})

@app.route("/", methods=["GET"])
def index():
    return "<h1>Potato is ready.</h1>\n" \
            "<h1>Ready to eat!</h1>\n" \
            "<h1>um yam yam yam yam yam</h1>" \

if __name__ == '__main__':
    event_queue = mp.Queue()

    p = Thread(target=processing_event, args=(event_queue,))
    p.start()
    print("subprocess started")

    app.run(port=5000, debug=True)
    p.join()





