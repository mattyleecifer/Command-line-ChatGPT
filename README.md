# TerminalGenie

Note: This project has now been rewritten in Golang and combined into [AgentSmith](https://github.com/mattyleecifer/AgentSmith).

An implementation of the ChatGPT API in the command-line with some extra features to make it easy to use.

# Features
To use any of these features, just type the command into the terminal. 

| Function | Command | Description |
| --- | --- | --- |
| Code Mode | `code` | Generates a list of steps first before outputting code. The function is interactive, so you can discuss the plan and generated code with the bot and regenerate new plans and new code based on the discussion. |
| Copy Last Output | `copy` | Copies the last output from the bot into clipboard. |
| Paste Query | `paste` | Pastes your clipboard as a query. This way you can craft prompts in a text editor for multi-line queries. |
| Save Chat | `save` | Saves the chat into a json file with the filename YYYYMMDDHHMM.json. |
| Load Chat | `load <filename>` | Loads files. |
| Line Selection | `@`, `sel`, or `select` | Allows you to select lines to delete in case the chat is getting too long and you want to save on costs. Can delete individual lines (eg 1, 3) or a range of lines (eg 1-3) |
| Delete Chat History | `!`, `del`, or `delete` | Clears the chat log and starts fresh. |
| Help Menu | `help` | Brings up a help menu with this information. |
| Quit Program | `q` or `quit` | Exits the program. |
| Token Counter || The program will tell you how many tokens you have used for the current session and also the estimated cost. |
|<img width=210/>|<img width=240/>||

# Installation
1. Make sure you have Python3 installed on your system. If you don't have it installed, download and install it from [here](https://www.python.org/downloads/).

2. Clone this GitHub repository to your local machine by running the following command in your terminal:

   ```
   git clone https://github.com/mattyleecifer/TerminalGenie.git
   ```
   Or click the green 'Code' button on the top right of this repository and choose 'Download ZIP' (or whatever option you prefer)
3. Navigate to the project directory on your terminal.
   ```
   cd /installation/directory
   ```
4. Run the following command to install all the necessary packages:
   ```
   pip install -r requirements.txt
   ```
5. Run 'setkey.py' to set the API key - if you don't have an OpenAI API key, you can get one [here](https://platform.openai.com/account/api-keys).
   ```
   python3 setkey.py
   
   or 
   
   py setkey.py
   ```
6. Run tg.py in terminal
   ```
   python3 tg.py
   
   or 
   
   py tg.py
   ```
