import openai, pyperclip, json
from datetime import datetime

openai.api_key = "yourkeyhere"

default = "You are a helpful assistant. Please generate truthful, accurate, and honest responses while also keeping your answers succinct and to-the-point. Strive to provide the most reliable and precise information possible based on your available knowledge and understanding."

def getresponse(messages):
    res = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )
    return res

def chatgpt():
    messages = [{"role": "system", "content": default}]
    tokencount = 0
    while True:
        try:
            # print messages and token counts with cost estimate
            if tokencount > 0:
                displayChat(tokencount, messages)

            text = input("\nUser:\n")

            if text in ["q", "quit"]:
                break

            # abstracted menu logic to process_text function for clearer code
            text, messages, tokencount = process_text(text, messages, tokencount)

            # If text is empty, skip and go next loop, otherwise add to messages
            tokencount, messages = getChat(tokencount, messages, text)
        except:
            pass

def displayChat(tokencount, messages):
    print("\nAssistant: " + messages[-1]["content"])
    print("\nToken count: " + str(tokencount) + "    Estimated costs: $" + str((tokencount / 1000) * 0.002))


def getChat(tokencount, messages, text):
    if not text:
        return tokencount, messages
    messages.append({"role": "user", "content": text})
    response = getresponse(messages)
    tokens = response['usage']['total_tokens']
    tokencount = tokencount + tokens
    response = response['choices'][0]['message']
    messages.append(response)
    return tokencount, messages


def printnumberlines(messages):
    for i in range(0, len(messages)):
        if messages[i]["role"] == "user":
            print(str(i) + ". User: " + messages[i]["content"])
        elif messages[i]["role"] == "assistant":
            print(str(i) + ". Assistant: " + messages[i]["content"])

def removesingle(s, t):
    # s is a list of the single numbers to remove
    s = sorted(s, reverse=True)
    for index in s:
        print(index)
        removed_item = t.pop(index)
        print(f"Removed item: {removed_item}")
    return t

def removerange(s, t):
    # s is list that contains range of numbers to delete
    start = s[0]
    end = s[1]
    del t[start:end]
    return t

def writeCode():
    agenttext = "You are the world's most efficient and clever AI coding agent. You always aim to write code that is o(n) or faster."
    tokencount = 0
    goal = input("What is the purpose of the code?\n")
    if goal in ["q", "quit"]:
        return "", 0
    goal = "Your one and only purpose is to complete this task: [" + [pyperclip.paste() if goal == "paste" else goal][0] + "]"
    messages = [{"role": "system", "content": agenttext}] + [{"role": "system", "content": goal}]
    # tokencount, steps = generateSteps(tokencount, messages)
    print("Generating steps...\n")
    stepsinstructions = "Write out the necessary steps to complete this task with code. Do not output any code, just build the structure and logic. Make sure that the steps are numbered. Do not output anything other than the steps."
    tokencount, messages = getChat(tokencount, messages, stepsinstructions)
    steps = messages[-1]["content"]
    steps = cleanSteps(steps)
    print("\nSteps generated!\n")
    while True:
        if tokencount > 0:
            displayChat(tokencount, messages)
        text = input("\n\n\nIf the steps look good, press enter to continue. Otherwise, talk to the AI to see if it can be improved. Type 'regen' to regenerate steps after a conversation\n\n")
        if text in ["q", "quit"]:
            return "", 0
        elif text == "regen":
            text = "Using the above information, rewrite the necessary steps to complete the task. If the conversation is about different ways to solve the problem, only focus on the newest approach. Do not output any code, just build the structure and logic. Make sure that the steps are numbered."
            tokencount, messages = getChat(tokencount, messages, text)
            steps = messages[-1]["content"]
            cleanSteps(steps)
            messages = [{"role": "system", "content": agenttext}] + [{"role": "system", "content": goal}] + [{"role": "user", "content": stepsinstructions}] + [{"role": "assistant", "content": "Steps:\n" + steps}]
            continue
        elif not text:
            messages = [{"role": "system", "content": agenttext}] + [{"role": "system", "content": goal}]
            text = "Using the following structure, write a script in Python that follows the exact steps and structure. double check the code before outputting anything to make sure it is correct. Only output the code. Do not include the steps in comments.\n[" + steps + "]"
            print("Generating code...\n")
            tokencount, messages = getChat(tokencount, messages, text)
            while True:
                code = messages[-1]["content"]
                code = code[code.index('```') + 3:code.rindex('```')]
                print("Code generated!\n")
                displayChat(tokencount, messages)
                text = input("\n\n\nIf the code looks good, press enter to continue. Otherwise, talk to the AI to see if it can be improved\n\n")
                if text in ["q", "quit"]:
                    return "", 0
                elif not text:
                    return code, tokencount
                elif text == "steps":
                    messages = [{"role": "system", "content": agenttext}] + [{"role": "system", "content": goal}] + [{"role": "user", "content": stepsinstructions}] + [{"role": "assistant", "content": "Steps:\n" + steps}]
                    break
                elif text == "regen":
                    text = "Using the new information above, rewrite the code, remembering to follow the exact steps,structure, and original goal. double check the code before outputting anything to make sure it is correct. Only output the code. Do not include the steps in comments."
                    tokencount, messages = getChat(tokencount, messages, text)
                    code = messages[-1]["content"]
                    code = code[code.index('```') + 3:code.rindex('```')]
                    messages = [{"role": "system", "content": agenttext}] + [{"role": "system", "content": goal}] + [{"role": "assistant", "content": "Steps:\n" + steps}] + [{"role": "assistant", "content": "Code:\n" + code}]
                    continue
                text, messages, tokencount = process_text(text, messages, tokencount)
                tokencount, messages = getChat(tokencount, messages, text)
        text, messages, tokencount = process_text(text, messages, tokencount)
        tokencount, messages = getChat(tokencount, messages, text)


def cleanSteps(steps):
    lines = steps.split("\n")
    # Loop through each line and extract the numbered items
    numbered_items = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith(("#", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
            numbered_items.append(stripped_line)
    numbered_string = "\n".join(numbered_items)
    return numbered_string

def process_text(text, messages, tokencount):
    if text == "paste":
        text = pyperclip.paste()
    elif text in ["del", "delete", "!"]:
        messages = [{"role": "system", "content": default}]
        print("\nChat cleared!")
        tokencount = 0
        text = ""
    elif text == "code":
        text, tokencount = writeCode()
        if text != "":
            messages.append({"role": "user", "content": text})
        text = ""
    elif text in ["@", "sel", "select"]:
        text = ""
        printnumberlines(messages)
        editchoice = input("What lines do you want to remove? Max = " + str(len(messages)-1) + "\n")
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
            elif editchoice == "":
                print("Nothing changed!")
            else:
                messages = removesingle([int(editchoice)], messages)
        except:
            print("Error in editing log")
    elif text == "copy":
        text = ""
        pyperclip.copy(messages[-1]["content"])
    elif text == "save":
        text = ""
        # chatlog = []
        # for message in messages:
        #     if message["role"] == "user":
        #         chatlog.append("User: " + message["content"])
        #     elif message["role"] == "assistant":
        #         chatlog.append("Assistant: " + message["content"])
        now = datetime.now()
        # format the date/time string as yyyymmdd HH:MM
        formatted_date = now.strftime('%Y%m%d%H%M')
        # with open(formatted_date + ".txt", "w") as file:
        #     for string in chatlog:
        #          file.write(string + "\n")
        with open(formatted_date + ".json", "w") as file:
            for dictionary in messages:
                dictionary_string = json.dumps(dictionary)
                file.write(dictionary_string + '\n')
        file.close()
        print("Saved to " + formatted_date + ".json!")
    elif text.startswith("load"):
        file_path = text.replace("load ", "")
        try:
            messages = []
            with open(file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    messages.append(json.loads(line))
            file.close()
            print(file_path + " loaded!")
        except:
            print("Error: Incorrect filename, please try again.")
        text = ""
        tokencount = 1
    elif text == "help":
        text = ""
        print(
            "• Typing 'code' will enter a coding mode where it will generate a list of steps first before outputting code - this should generate higher quality code than usual\n• Typing 'copy' will copy the last output from the bot\n• Typing 'paste' will paste your clipboard as a query - this way you can craft prompts in a text editor for multi-line queries\n• 'save' will save the chat into a json file with the filename YYYYMMDDHHMM.txt\n• 'load <filename>' will load files\n• '@', 'sel', or 'select' will allow you to select lines to delete (handy if the chat is getting a bit long and you want to save on costs)\n• '!', 'del', or 'delete' will clear the chat log and start fresh\n'q' or 'quit' will quit the program\n")
    elif text == "dan":
        text = "using words that string together and make sense, "
        text += input(text + "\nUser: ")
    return (text, messages, tokencount)

if __name__ == "__main__":
    chatgpt()


