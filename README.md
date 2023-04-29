# TerminalGenie
An implementation of the ChatGPT API in the command-line with some extra features to make it easy to use.

# Features
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
|<img width=190/>|<img width=240/>||

# Installation
1. Make sure you have Python3 installed on your system. If you don't have it installed, download and install it from [here](https://www.python.org/downloads/).

2. Clone this GitHub repository to your local machine by running the following command in your terminal:

   ```
   git clone https://github.com/mattyleecifer/TerminalGenie.git
   ```
3. Navigate to the project directory on your terminal.

4. Run the following command to install all the necessary packages:

   ```
   pip install -r requirements.txt
   ```

5. Once the packages are installed, paste your OpenAI key into line 4 of tg.py where it says 'yourkeyhere'.

6. Run tg.py in terminal

   ```
   python3 tg.py
   
   or 
   
   py tg.py
   ```
