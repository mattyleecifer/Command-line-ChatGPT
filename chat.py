import openai, pyperclip
now = datetime.now()

openai.api_key = "yourkeyhere"

def getresponse(messages):
    messages = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )
    return messages

def chatgpt():
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    while True:
        print("\n\n")
        for message in messages:
            if message["role"] == "user":
                print("User: " + message["content"])
            elif message["role"] == "assistant":
                print("Assistant: " + message["content"])
        text = input("\nUser:\n")
        if text == "paste":
            text = pyperclip.paste()
            continue
        if text in ["del", "delete", "!"]:
            messages = [{"role": "system", "content": "You are a helpful assistant."}]
            print("\nChat cleared!")
            continue
        if text in ["@", "sel", "select"]:
            printnumberlines(messages)
            editchoice = input("What lines do you want to remove? Enter range (eg. 1:4 or 1-4) or list (eg. 1,4,5)")
            try:
                if ":" in editchoice:
                    editchoice = editchoice.split(":")
                    editchoice = [int(x) for x in editchoice]
                    messages = removerange(editchoice, messages)
                    continue
                elif "-" in editchoice:
                    editchoice = editchoice.split("-")
                    editchoice = [int(x) for x in editchoice]
                    messages = removerange(editchoice, messages)
                    continue
                elif "," in editchoice:
                    editchoice = editchoice.split(",")
                    editchoice = [i for i in editchoice if i != ""]
                    editchoice = [int(x) for x in editchoice]
                    messages = removesingle(editchoice, messages)
                    continue
                else:
                    print("Nothing changed!")
                    continue
            except:
                print("Error in editing log")
                continue
         if text == "save":
            chatlog = []
            for message in messages:
                if message["role"] == "user":
                    chatlog.append("User: " + message["content"])
                elif message["role"] == "assistant":
                    chatlog.append("\nAssistant: " + message["content"])
            now = datetime.now()
            # format the date/time string as yyyymmdd HH:MM
            formatted_date = now.strftime('%Y%m%d %H:%M')
            with open(formatted_date + ".txt", "w") as file:
                for string in chatlog:
                    file.write(string + "\n")
            continue
        if text == "copy":
            printnumberlines(messages)
            pyperclip.copy(messages[-1]["content"])
            continue
        messages.append({"role": "user", "content": text})
        response = getresponse(messages)
        response = response['choices'][0]['message']
        messages.append(response)

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
    return result

def removerange(s, t):
    # s is range of numbers to delete
    start = s[0]
    end = s[1]
    del t[start:end]
    return result

if __name__ == "__main__":
    chatgpt()


