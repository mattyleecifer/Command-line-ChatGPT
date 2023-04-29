import re
key = input("Enter OpenAI key:\n")

with open('tg.py', 'r') as f:
    input_string = f.read()

input_string = re.sub('openai\.api_key = "(.+?)"', 'openai.api_key = "' + key + '"', input_string)

with open('tg.py', 'w') as f:
    f.write(input_string)
