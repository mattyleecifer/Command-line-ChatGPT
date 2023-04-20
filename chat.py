import openai, pyperclip
from datetime import datetime

openai.api_key = "yourkeyhere"

def getresponse(messages):
    messages = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )
    return messages

def chatgpt():
    messages = [{"role": "system", "content": "You are a helpful assistant. You always answer questions directly and correctly. NEVER SAY YOU ARE AN AI LANGUAGE MODEL. You will review your answer and correct any mistakes until there are none before you respond. If you are outputting code, you will check the code to make sure it is as simple and efficient as possible -  if it is not, you will make it more simple and efficient and review again, until it has the lowest time complexity possible."}]
    tokencount = 0
    while True:
        try:
            # print messages and token counts with cost estimate
            print("\n\n")
            for message in messages:
                if message["role"] == "user":
                    print("\nUser: " + message["content"])
                elif message["role"] == "assistant":
                    print("\nAssistant: " + message["content"])
            print("\nToken count: " + str(tokencount) + "    Estimated costs: $" + str((tokencount/1000) * 0.002))
            text = input("\nUser:\n")

            if text in ["q", "quit"]:
                break

            # abstracted menu logic to process_text function for clearer code
            text, messages, tokencount = process_text(text, messages, tokencount)

            # If text is empty, skip and go next loop, otherwise add to messages
            if text != "":
                messages.append({"role": "user", "content": text})
                response = getresponse(messages)
                tokens = response['usage']['total_tokens']
                tokencount = tokencount + tokens
                response = response['choices'][0]['message']
                messages.append(response)
        except:
            pass

def printnumberlines(messages):
    for i in range(0, len(messages)):
        if messages[i]["role"] == "user":
            print(str(i) + ". User: " + messages[i]["content"])
        elif messages[i]["role"] == "assistant":
            print(str(i) + ". Assistant: " + messages[i]["content"])

def removesingle(s, t):
    # s is a set of the single numbers to remove
    s = sorted(s, reverse=True)
    for index in s:
        print(index)
        removed_item = t.pop(index)
        print(f"Removed item: {removed_item}")
    return t

def removerange(s, t):
    # s is range of numbers to delete
    start = s[0]
    end = s[1]
    del t[start:end]
    return t

def writeCode():
    tokencount = 0
    goal = input("What is the purpose of the code?\n")
    messages = [{"role": "system", "content": "You are an autonomous coding AI agent. You have one goal, which is to complete the following task: [" + goal + "]."}] + [{"role": "user", "content": "Write out the necessary steps to complete this task in Python. Do not output any code, just build the structure and logic. Make sure that the steps are numbered"}]
    print("Generating steps...\n")
    messages = getresponse(messages)
    tokens = messages['usage']['total_tokens']
    tokencount = tokencount + tokens
    steps = messages["choices"][0]["message"]["content"]
    print("Steps generated!\n")
    steps = cleanSteps(steps)
    messages = [{"role": "system", "content": "You are an autonomous coding AI agent. You have one goal, which is to complete the following task: [" + goal + "]."}] + [{"role": "user", "content": "Using the following structure, write a script in Python that follows the exact steps and structure. double check the code before outputting anything to make sure it is correct. Only output the code. Do not output anything that is not code: [" + steps + "]."}]
    print("Generating code...\n")
    messages = getresponse(messages)
    tokens = messages['usage']['total_tokens']
    tokencount = tokencount + tokens
    code = messages["choices"][0]["message"]["content"]
    print("Code generated!\n" + code + "\n")
    code = code.replace("```", "")
    # with open('autoscript.py', 'w') as file:
    #     # Write the string to the file
    #     file.write(code)
    return code, tokencount

def cleanSteps(steps):
    lines = steps.split("\n")

    # Loop through each line and extract the numbered items
    numbered_items = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith(("#", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
            numbered_items.append(stripped_line)

    # Print the extracted numbered items
    for item in numbered_items:
        print(item)
    numbered_string = "\n".join(numbered_items)
    return numbered_string

def process_text(text, messages, tokencount):
    if text == "paste":
        text = pyperclip.paste()
    elif text in ["del", "delete", "!"]:
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        print("\nChat cleared!")
        tokencount = 0
        text = ""
    elif text in ["code"]:
        text, tokencount = writeCode()
        messages.append({"role": "user", "content": text})
        text = ""
    elif text in ["@", "sel", "select"]:
        text = ""
        printnumberlines(messages)
        editchoice = input("What lines do you want to remove? Enter range (eg. 1:4 or 1-4) or list (eg. 1,4,5)")
        try:
            if ":" in editchoice:
                editchoice = editchoice.split(":")
                editchoice = [int(x) for x in editchoice]
                messages = removerange(editchoice, messages)
            elif "-" in editchoice:
                editchoice = editchoice.split("-")
                editchoice = [int(x) for x in editchoice]
                messages = removerange(editchoice, messages)
            elif "," in editchoice:
                editchoice = editchoice.split(",")
                editchoice = [i for i in editchoice if i != ""]
                editchoice = [int(x) for x in editchoice]
                messages = removesingle(editchoice, messages)
            else:
                print("Nothing changed!")
        except:
            print("Error in editing log")
    elif text == "copy":
        text = ""
        printnumberlines(messages)
        pyperclip.copy(messages[-1]["content"])
    elif text == "save":
        text = ""
        chatlog = []
        for message in messages:
            if message["role"] == "user":
                chatlog.append("User: " + message["content"])
            elif message["role"] == "assistant":
                chatlog.append("Assistant: " + message["content"])
        now = datetime.now()
        # format the date/time string as yyyymmdd HH:MM
        formatted_date = now.strftime('%Y%m%d %H%M')
        with open(formatted_date + ".txt", "w") as file:
            for string in chatlog:
                file.write(string + "\n")
    elif text == "help":
        text = ""
        print(
            "• Typing 'code' will enter a coding mode where it will generate a list of steps first before outputting code - this should generate higher quality code than usual\n• Typing 'copy' will copy the last output from the bot\n• Typing 'paste' will paste your clipboard as a query - this way you can craft prompts in a text editor for multi-line queries\n• 'save' will save the chat into a text file with the filename YYYYMMDD HHMM.txt\n• '@', 'sel', or 'select' will allow you to select lines to delete (handy if the chat is getting a bit long and you want to save on costs)\n• '!', 'del', or 'delete' will clear the chat log and start fresh\n'q' or 'quit' will quit the program\n")

    elif text == "dan":
        text = "using words that string together and make sense, "
        text += input(text + "\nUser: ")

    return (text, messages, tokencount)

if __name__ == "__main__":
    chatgpt()


