
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import sys


import time
import threading

import requests

import os
import re
import random

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
    r =  requests.post("http://localhost:11434/api/chat", json=payload, timeout=222222)
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
winnings_lock = threading.Lock()
in_progress_pairs = set()

def pair_key(word, word2):
    return tuple(sorted((word, word2)))

def save_winnings_locked():
    with open(f"horriblewords2.json","w") as fing:
        fing.write(json.dumps(winnings,indent=4,ensure_ascii=False))

def choose_word2(word):
    failedcounter = 0
    max_failed = 1_000_0000
    while failedcounter < max_failed:
        word2 = random.choice(wordslist)
        key = pair_key(word,word2)
        with winnings_lock:
            winnings.setdefault(word,{})
            already_done = word2 in [word,*list(winnings[word].keys())]
            already_complete = len(winnings.get(word2,{})) == desiredlen
            already_running = key in in_progress_pairs
            if already_done or already_complete or already_running:
                failedcounter += 1
                continue
            winnings.setdefault(word2,{})
            in_progress_pairs.add(key)
            return word2
    print("done")
    raise RuntimeError(f"could not find another word to compare with {word!r}")

def rank_word(word):
    # random.shuffle(wordslist2)
    with winnings_lock:
        winnings.setdefault(word,{})
    while True:
        with winnings_lock:
            if len(winnings[word]) == desiredlen:
                return word
        word2 = choose_word2(word)
        try:
            done = False
            while not done:
                try:
                    answer = asknicely(word,word2)
                    assert answer in ["text1","text2","none"]
                except Exception as e:
                    print("broke",e)
                    continue 
                done = True
            with winnings_lock:
                if len(winnings[word]) != desiredlen and word2 not in winnings[word] and len(winnings.get(word2,{})) != desiredlen:
                    winnings[word][word2] = answer
                    if answer == "text1":
                        winnings[word2][word] = "text2"
                    elif answer == "text2":
                        winnings[word2][word] = "text1"
                    else:
                        winnings[word2][word] = "none"
                    print(f"{word} | {word2} {answer}")
                    save_winnings_locked()
        finally:
            with winnings_lock:
                in_progress_pairs.discard(pair_key(word,word2))

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(rank_word,word) for word in list(winnings)]
    for future in as_completed(futures):
        future.result()
