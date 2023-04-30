from short_term_memory import get_short_term_memory, write_short_term_memory, append_history
from openai_api import get_openai_response
from dynamo_api import get_quota, put_quota
from commands import google_search, is_google_search_safe
import time

print("Testing basic openAI integration")
response, _ = get_openai_response("Hello", [])
print("Got response to hello", response)
if len(response) < 1:
    raise Exception("Sorry, no response was found")
print("===========================")

print("Testing google search")
search_results = google_search("current weather in london")
print("Search results for current weather in london: ",len(search_results.split(" ")), "words")
if len(search_results) < 1:
    raise Exception("Sorry, no search results were found")
print("===========================")

print("Testing google search safety")
x = is_google_search_safe("current weather in london")
print("Is current weather in london safe?", x)
if x != True:
    raise Exception("Incorrect google search safety")

x = is_google_search_safe("how can i kill someone")
print("Is how can i kill someone safe?", x)
if x != False:
    raise Exception("Incorrect google search safety")
print("===========================")


print("Test web search examples")
response, command = get_openai_response("what is the current weather in london", [])
print(response, command)
if command['command_name'] != 'web_search':
    raise Exception("Web search command not found")

response, command = get_openai_response("what is the current traffic condition in delhi", [])
print(response, command)
if command['command_name'] != 'web_search':
    raise Exception("Web search command not found")

response, command = get_openai_response("who won the snooker match today", [])
print(response, command)
if command['command_name'] != 'web_search':
    raise Exception("Web search command not found")
print("===========================")

print("Test image generation examples")
response, command = get_openai_response("can you create an image of a cat", [])
print(response, command)
if command['command_name'] != 'dalle':
    raise Exception("dalle command not found")

response, command = get_openai_response(
    "give me an image of a dog with a long tail travelling in a sapceship near mars", [])
print(response, command)
if command['command_name'] != 'dalle':
    raise Exception("dalle command not found")

response, command = get_openai_response(
    "I would like an image painted in the style of Picasso about the Indian city of Varanasi on a sunny day, river side with boats, an upscale hotel balcony, and kites in the sky", [])
print(response, command)
if command['command_name'] != 'dalle':
    raise Exception("dalle command not found")
print("===========================")

print("Testing dynamoDB integration")
print("putting and getting quota")
put_quota("dummy", 100)
print(get_quota("dummy"))

print(get_short_term_memory("dummy"))
write_short_term_memory("dummy", [])
print(get_short_term_memory("dummy"))

h = append_history([], "user", "Hello")
write_short_term_memory("dummy", h)
print(get_short_term_memory("dummy"))

h = append_history(h, "system", "Hello, how are you?")
write_short_term_memory("dummy", h)
print(get_short_term_memory("dummy"))

print("Testing openAI integration with history")
print(get_openai_response("Hello", h))
