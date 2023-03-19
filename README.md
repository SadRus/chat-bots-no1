# Dvmn task notifications telegram bot.
### Description

Create a telegram bot, that will send task notifications if code was reviewed by mentor.

### Objective of project

The script is written for educational purposes within online courses for web developers [dvmn.org](https://dvmn.org/).

### Installing

Python3 must be installed. 
Use `pip` (or `pip3`) for install requirements:
```
pip install -r requirements.txt
```

### Enviroment

You needs to create .env file for enviroment variables in main folder.

- `DVMN_TOKEN` - dvmn token, you can get it here: https://dvmn.org/api/docs/  
- `TG_BOT_TOKEN` - needs register a bot in telegram via @BotFather: https://t.me/BotFather
- `TG_CHAT_ID` - yours chat_id / user_id, you can check it via @userinfobot: https://t.me/userinfobot

### Usage
Before start the script, needs activate your bot via `/start` command in chat.

From scripts folder:
```
python(or python3) main.py
```
Alternate arguments:
- **-h / --help** - display shortly description of script and arguments.
- **-ci / chat_id** - yours chat_id / user_id (by default use enviroment variable 'TG_CHAT_ID').  

Running example with arguments:  
`python main.py --ci 123456`

### Example
After running the script, you can check its work yourself by submitting the work for review and then canceling it.
- Send for review  
![image](https://user-images.githubusercontent.com/79669407/226210713-03f99181-eb63-471b-8a27-c6f6468d623e.png)  
- Return it back  
![image](https://user-images.githubusercontent.com/79669407/226210783-fe2f5c43-56ba-46f4-a82b-c446e5efd7e8.png)  
- Check telegram  
![image](https://user-images.githubusercontent.com/79669407/226210848-b462c3a6-5a72-4e42-afb8-48ce11d72448.png)






