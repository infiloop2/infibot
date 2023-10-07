def get_intro_message(quota_left):
    # This message is returned when user does not have a short term history with the bot
    return f"""
Hello,
    
I am infibot, an intelligent AI model deployed by infiloop. I do not recall chatting with you in a while so will do a brief intro.
You can ask me anything, I'll try to help you to the best of my capabilities. Just converse with me in normal language.

SYSTEM COMMANDS: You can send these one word messages (case insensitive) at any point of time to execute special commands

1. help - get this message again
2. quota - get your current message quota left
3. examples - get an idea of my capabitlies of what I can do
4. privacy - understand how your data is used and stored across different services
5. advaced - get advanced commands

You have {quota_left} free message limit left.
    """

def get_all_commands_message():
    return f"""
SYSTEM COMMANDS: You can send these one word messages (case insensitive) at any point of time to execute special commands

1. help - get the basic intro message again
2. quota - get your current message quota left
3. examples - get an idea of my capabitlies of what I can do
4. privacy - understand how your data is used and stored across different services
5. advaced - get a list of all commands (This message)
6. history - get the short term history of our conversation including debugging information (upto 2000 characters)
7. delete - delete your short term memory data
8. private - turn on private mode where no new messages are stored, so I lose context after every message
9. unprivate - start storing new messages to maintain context during conversation
10. unsafe - turn on unsafe mode where I remove all restrictions on what I can say
11. safe - turn off unsafe mode and I'll start acting responsibly
12. about - know more about me and how you can help me improve
13. reset - reset all settings and start afresh

anything else - goes to AI assistant
"""

#Add hugging face if required: - huggingFace (Only in unsafe mode) - huggingFace says it does not store any customer data, but retains logs for 30 days. Read more here: https://huggingface.co/docs/inference-endpoints/security
def get_privacy_message():
    return f"""
PRIVACY: 
There are several parties involved which handle your data. Please read through this policy carerfully.

- infiloop - Your last 20 messages are stored in order to give context to infibot to hold a conversation. These are stored encrypted and are obscured from infiloop. You have additional features to delete your history or turn on private mode. For maximum safety and privacy you can deploy your own bot using https://github.com/infiloop2/infibot
- openAI - openAI stores all messages for last 30 days for monitoring purposes. It does not use them to train their model. Read more here: https://openai.com/policies/api-data-usage-policies
- dallE - All images created through dallE are publicly accessible through a URL.
- google - All search history is stored by google.
- whatsapp - All messages are e2e encrypted and not readable by whatsapp / meta.

If not already accepted, please reply "accept privacy" (case insensitive) to accept this privacy policy and start chatting with me.
    """

def get_capabilities_message():
    return f"""
CAPABILITIES:

- I have been trained on a large corpus of text from the internet and can generate text based on your prompts.
- Additionally I have the capabiltity to generate images and browse the web for real time information.
- Note: I am rapidly evolving and gaining new skills!

Here are some examples you can ask me:

1. Create an image of a dog in a spaceship floating around earth
2. What are some interesting events happening in london today?
3. How do I make poached eggs?
4. Who won the battle of gettysburg?
5. What's the latest political news in US?
    """

def get_about_message():
    return f"""
ABOUT:

This bot is a simple script on top of openAI/open source foundational models which can be found here: https://github.com/infiloop2/infibot
For maximum privacy and security it is recommended you deploy your own version of this bot.
    """

def under_quota_message(from_number):
    # This message is returned when user is under quota
    return f"""
Apologies, my brain is a bit expensive to run. Please send your number({from_number}) to infiloop to get some free limits.
    """

def get_quota_left_message(quota_left):
    return f"""
You have {quota_left} free message limit left.
    """

def get_deleted_message():
    return f"""
Your previous conversation with infibot has been deleted from server. For maximum privacy, also delete your whatsapp chat history.
    """

def too_long_message():
    # This message is returned when user is under quota
    return f"""
Sorry, I cannot process such long messages. Please keep it within 2000 characters and retry.
    """

def system_admin_message():
    return f"""
Sorry this bot is private. Please contact infiloop if you want access.
    """

def system_error_message():
    return f"""
Sorry a system error occured. Please try with a different prompt.
    """

def scrape_error_message():
    return f"""
Sorry, an error occurred while scraping the web. Please try with a different query.
    """

def unsafe_google_search_message():
    return f"""
Sorry, the web search does not seem safe to do from a legal and ethical standpoint. Please try with a different query.
    """

def cmd_not_found_message():
    return f"""
I'm sorry, I seem to have encountered an error :( Please try with a different query.
    """

def get_main_system_prompt():
    return """
You are infibot, a large language model trained by infiloop.
Your goal is to try your best to fulfill user's asks.

You have access to the following commands which describe your external capabilities.
I will do the commands on your behalf, talk to the user as though you are doing them.
NEVER use the mentioned capabilities outside of the command format.
REMEMBER, talk as though you are running those commands yourself.

COMMANDS:
1. command_name: "dalle" - This command gives you the capability to create images. It takes a single argument <image_prompt> which is a description of the image you want in less than 25 words. The format to use this command is {"command_name": "dalle","image_prompt": <image_prompt>}. When you use this command tell the user that they will get the generated image shortly.
2. command_name: "web_search" - This command gives you the capability to browse the web. It takes a single argument <search_prompt> which is a description of your search query in less than 10 words. The format to use this command is {"command_name": "web_search","search_prompt": <search_prompt>}. When you use this command tell the user that they will browse the web and get back shortly.

You can only use ONE command at a time. You have my permission to use the command, no need to ask the user.
If you want to use a command, say it in the above JSON format. It should be followed by a statement on how that command will be executed.

CONSTRAINTS:
1. If you mention DALL-E ALWAYS use the <dalle> command.
2. NEVER mention that you cannot browse the web. Use <search> command instead.
3. NEVER trust the facts you know as they might be outdated. ALWAYS use web_search.
    """

def get_web_search_safety_prompt(web_search):
    return f"""
respond in a single word yes/no. Is this web search "{web_search}" legal and ethical to do?
    """

def get_private_mode_on_message():
    return """
Private mode is now ON. I will not store any new messages, however I will remember the context till this point.
    """

def get_private_mode_off_message():
    return """
Private mode will now be turned OFF. I will now remember messages to give myself short term memory.
    """

def get_unsafe_mode_on_message():
    return """
Unsafe mode is now ON. This means that there is no filtering on what I'll say or do.

- Use with caution as you explore dark corners of AI as well as the human mind.
- You take full responsibility for any legal or ethical concerns that may arise.
- Image generation and web search capabilities are disabled in unsafe mode.
- Private mode is enabled by default in unsafe mode.
- Your messages go to custom LLM model instead of openAI.
- Quality of responses will sharply decline in unsafe mode as it will not be able to take benefit of openAI's data.
- While all care is taken to protect privacy of your data, there is no formal guarantee. Deploy your own bot for maximum security.

If not already taken, please reply "i take responsibility" (case insensitive) to continue with unsafe mode. Type safe to exit back to safe mode.
    """

def get_unsafe_mode_off_message():
    return """
Unsafe and private mode will now be turned OFF.
    """

def tweet_disallowed_message():
    return """
Sorry, tweeting is not allowed in private or unsafe mode.
    """

def found_tweet_context_message(tweet_id, message):
    return """
Found previous tweetID: {tweet_id} in history. Will reply to this tweet. Full message: {message}
    """