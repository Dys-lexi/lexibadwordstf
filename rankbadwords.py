from gevent import monkey
import json
import sys
from datetime import datetime
import datetime as pants
import functools
import time
import threading
import requests
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from flask import Flask, jsonify, request, send_from_directory, send_file, Response
import os
import re
from steamid_converter import Converter
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from psycogreen.gevent import patch_psycopg
import random
from initsql import querywrapper
from tempurature import recalltemp
from cachetools import cached, LRUCache, TTLCache
from slurcloud import makewordcloud
chatfilterroot = "./chatfilters/"

def pullbadwords():
    files = os.listdir(chatfilterroot)
    wordslist = []
    for file in files:
        with open(f"{chatfilterroot}{file}","r") as fing:
            for line in fing.readlines():
                stripped = line.strip()
                if stripped and not stripped.startswith("###") and len(stripped):
                    wordslist.append(stripped)

    wordslist = [w for w in [word.replace('\x00', '') for word in wordslist if word.replace('\x00', '') not in  ['%', '_', '']]]
    return wordslist


def asknicely(text1,text2):
    question = f"""You are given with two texts. Your task is to compare which text is more toxic.

Options:

- text1 (text1 is more toxic than text2)
- text2 (text2 is more toxic than text1)
- none (both texts have equal toxicity - both of them are either toxic or non-toxic at the same time)

You must return ONLY one of the options. Do not add any explanations or additional information - the options being 'text1' 'none' and 'text2'
only respond 'none' if you think they are actually the same

text1: {text1}
text2: {text2}
"""

    payload = {
        "model": "qwen3.6:latest",
        "messages": [
            # *list(map(lambda x: {"role":"assistant","content":x} ,messagesisent[-20:] )),
            # {"role": "system", "content": system_prompt},

            {"role": "user", "content": question}
        ],
        "stream": False,
        "keep_alive":"12h",
        "options":{"temperature":0}
    }
    r =  requests.post("http://192.168.18.83:11434/api/chat", json=payload, timeout=222222)
    r.raise_for_status()
    print(json.dumps(r.json(),indent=4))
    return r.json()["message"]["content"]

wordslist = pullbadwords()
desiredlen = 20
with open(f"horriblewords.json","r") as fing:
    winnings = json.load(fing)
winnings = dict(filter(lambda x:  len(winnings.get(x[0],{})) != desiredlen, list(map(lambda x: [x,winnings.get(x,{})],wordslist))))

# print("e",list(map(lambda x: [x,winnings.get(x,{})],wordslist)))

# winnings = {}
print("weee")
for word in winnings:
    # random.shuffle(wordslist2)
    winnings.setdefault(word,{})
    while len(winnings[word]) != desiredlen:
        failedcounter = 0
        while ((word2 := random.choice(wordslist))  in [word,*list(winnings[word].keys())] or len(winnings.get(word2,{})) == desiredlen) and failedcounter < 1_000_0000: failedcounter += 1
        if failedcounter > 999_999:
            print("done")
            raise
        winnings.setdefault(word2,{})
        done = False
        while not done:
            try:
                answer = asknicely(word,word2)
                assert answer in ["text1","text2","none"]
                winnings[word][word2] = answer
                if answer == "text1":
                    winnings[word2][word] = "text2"
                elif answer == "text2":
                    winnings[word2][word] = "text1"
                else:
                    winnings[word2][word] = "none"    
            except Exception as e:
                print("broke",e)
                continue 
            done = True
        print(f"{word} | {word2} {answer}")

        with open(f"horriblewords2.json","w") as fing:
            fing.write(json.dumps(winnings,indent=4,ensure_ascii=False))


