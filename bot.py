import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import requests
import random

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'],'/slack/events',app)

client = slack. WebClient(token = os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call('auth.test')['user_id']

# @slack_events_adapter.on('message')
# def message(payload):
#     event = payload.get('event', {})
#     channel_id = event.get('channel')
#     user_id = event.get('user')
#     text = event.get('text')
#     if BOT_ID != user_id:
#         client.chat_postMessage(channel=channel_id, text=text)

@app.route('/getPS', methods = ['POST'])
def message_count():
    data = request.form
    data = data.to_dict()
    channel_id = data['channel_id']
    command = data['text'].split()
    cf = command[0]
    levels = {'b' : 0, 's' : 5, 'g' : 10, 'p' : 15, 'd' : 20, 'r': 25}
    if cf[0] in 'bsgpdr' and cf[1].isdigit() and 0 < int(cf[1]) <= 5:
        n = levels[cf[0]] + 6-int(cf[1])
        print(n)
        f = open('./problems/'+ str(n) +'.txt', 'r')
        p_list = f.read().split()
        p_num = random.choice(p_list)
        prob = '난이도 : '+ cf+'\nhttps://www.acmicpc.net/problem/' + p_num
        client.chat_postMessage(channel=channel_id, text=prob)
        return Response(), 200
    elif cf == 'delete':
        ts = ''
        for i in range(10):
            if client.conversations_history(channel=channel_id)['messages'][i]['user'] == 'U0375943YGH':
                ts = client.conversations_history(channel=channel_id)['messages'][i]['ts']
                break
        if ts != '':
            client.chat_delete(channel=channel_id, ts = ts)
        else:
            client.chat_postMessage(channel=channel_id, text='no Bot messages')
        return Response(), 200
    elif cf == 'range':
        if command[1][0] in 'bsgpdr' and command[1][1].isdigit() and 0 < int(command[1][1]) <= 5:
            if command[2][0] in 'bsgpdr' and command[2][1].isdigit() and 0 < int(command[2][1]) <= 5:
                n1 = levels[command[1][0]] + 6-int(command[1][1])
                n2 = levels[command[2][0]] + 6-int(command[2][1])
                min_n, max_n = min(n1,n2), max(n1,n2)
                p_list = []
                for i in range(min_n,max_n+1):
                    f = open('./problems/'+ str(i) +'.txt', 'r')
                    p_list.extend(f.read().split())
                p_num = random.choice(p_list)
                prob = '난이도 : '+ command[1] + '~' + command[2] +'\nhttps://www.acmicpc.net/problem/' + p_num
                client.chat_postMessage(channel=channel_id, text=prob)
        return Response(), 200
    else:
        client.chat_postMessage(channel=channel_id, text='wrong query')
        return Response(), 200
    
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = '30001', debug=True)
    
