# Dvmn task notifications telegram bot.
### Table of content:
1. [Description](#description)
2. [Objective of project](#objective-of-project)
3. [Installing](#installing)
4. [Enviroment](#enviroment)
5. [Usage](#usage)
6. [Example](#example)
7. [Deployment](#deployment-on-a-server)

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
- `LOGS_FOLDER` - destination folder for logs

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

### Deployment on a server

1. Log in to a server via username, server IP and password:  
`ssh {username}@{server IP}`
2. Clone repository. Advise to put the code in the `/opt/{project}/` folder
3. Put into the folder file with virtual enviroments `.env`
4. Create a virtual enviroment, use python(or python3):  
`python -m venv venv`
5. Install requirements, use pip(or pip3):  
 `pip install -r requirements`
6. Create a file(unit) in the `/etc/systemd/system` called like name project, e.g. `chat-bots-no1.service`, use:  
`touch /etc/systemd/system/chat-bots-no1.service`
7. Write the following config into it:  
    * Execstart - for start the sevice
    * Restart - auto-restart the service if it crashes
    * WantedBy - for start service within server
```
[Service]  
ExecStart=/opt/{project}/venv/bin/python3 /opt/{project}/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```  
8. Include the unit in the autoload list  
`systemctl enable echobot-example`
9. Reload systemctl  
`systemctl daemon-reload`
10. Start the unit  
`systemctl start chat-bots-no1`
11. Logs will writing into `/var/log/bot.log`
12. You can check the process, if the process is running it will show:  
`ps -aux | grep chat-bots-no1`
![image](https://user-images.githubusercontent.com/79669407/228650981-e6f8016a-40e6-4c4f-88ef-a3df6969d2fc.png)
13. if the bot is running it will send a message:  
![image](https://user-images.githubusercontent.com/79669407/228651407-0473a366-5cab-4ac8-a346-8e8435ce402d.png)

