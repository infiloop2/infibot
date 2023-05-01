import openai
# import tiktoken

import os
import re
import copy
import json
from system_messages import get_main_system_prompt, cmd_not_found_message

openai.api_key = os.environ.get("openai_token")
model = "gpt-3.5-turbo"

def get_openai_response(message, history, optimiseCommand=True):
    ai_response = ""
    command = None
    messages = [
        {"role": "system", "content": get_main_system_prompt()},
    ]
    limited_history = limit_history_tokens(history, 1500)
    for h in limited_history:
        messages.append({"role": h.get("role"),
                        "content": h.get("message")})
        
    if message is not None:
        messages.append({"role": "user", "content": message})

    try:
        ai_response, command = getChatCompletionResponseCommand(messages)
        if not optimiseCommand:
            return ai_response, command
        
        if expect_command(ai_response) and command is None:
            # Try to regenerate response with a nudge from the system
            messages.append({"role": "system", "content": "Please output the command in specified format"})
            ai_response, command = getChatCompletionResponseCommand(messages)
        
        if expect_command(ai_response) and command is None:
            ai_response = cmd_not_found_message()
    except Exception as _:
        ai_response = "I'm sorry, I encountered an error :("

    return ai_response, command

def getChatCompletionResponseCommand(messages):
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    ai_response = getResponsePreferCommand(completion["choices"])
    command = parse_command(ai_response)
    return ai_response, command

def expect_command(response):
    return re.search("dalle|dall-e|DALLE|DALL-E|web_search", response) is not None

def getResponsePreferCommand(choices):
    for choice in choices:
        resp = choice.message.get("content")
        if parse_command(resp):
            return resp
    return choices[0].message.get("content")

def parse_command(response):
    start = response.find('{"command_name":')
    while start != -1:
        end = response.find("}", start) + 1
        cmd = response[start:end]
        if is_json(cmd):
            cmd = json.loads(cmd)
            if cmd['command_name'] == "dalle" and cmd.get("image_prompt") is not None:
                return {
                    "command_name": "dalle",
                    "image_prompt": cmd.get("image_prompt")
                }
            if cmd['command_name'] == "web_search" and cmd.get("search_prompt") is not None:
                return {
                    "command_name": "web_search",
                    "search_prompt": cmd.get("search_prompt")
                }
        
        start = response.find('{"command_name":', end)
    return None


def limit_history_tokens(history, limit):
    limited = copy.deepcopy(history)
    while num_tokens_from_messages(limited) > limit:
        limited.pop(0)
    return limited


def num_tokens_from_messages(messages):
    # tiktoken times out on lambda, using a heuristic as a workaround
    # encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = 0
    for message in messages:
        # every message follows <im_start>{role/name}\n{content}<im_end>\n
        num_tokens += 4
        for key, value in message.items():
            if key == "timestamp":
                continue
            # Two times the number of words for well formed words
            num_tokens += len(value.split(" ")) * 2
            # num_tokens += len(encoding.encode(value))
            num_tokens += 2  # every reply is primed with <im_start>assistant

    return num_tokens


def run_dalle(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024",
    )
    image_url = response['data'][0]['url']
    return image_url


def is_json(str):
    try:
        _ = json.loads(str)
    except ValueError as _:
        return False
    return True
