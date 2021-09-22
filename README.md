## noicebot
multi-purpose discord bot written using discord.py

---
## requirements
* `python3`
* `discord.py`
* a `config/` folder

---
## installing discord.py
* Linux: `python3 -m pip install -U discord.py`
* Windows: `py -3 -m pip install -U discord.py`

---
## bot install and setup
* `git clone https://github.com/noicenoicebaby/noicebot.git`
* `cd noicebot/` changes directory to noicebot
* `mkdir config/` to make a config directory
* cd `config/` changes directory to config
* `nano api-key` copy down your API key that you were given by https://thedogapi.com/ or https://thecatapi.com/ and paste into the file
* `nano bot-token` copy down you bot token that you were give in the discord developer portal and paste into the file
* `nano welcomechannel-id` copy down your welcome channel id in your discord server and paste into this file
* `nano goodbyechannel-id` copy down your welcome goodbye id in your discord server and paste into this file
* `nano warns.json` leave this file blank
* `nano customprefix.json` and add a `{}` to the file.
* `nano blacklist.json` and add `["words", "of", "your", "choice"]` for them to be blacklisted. 
* `python3 bot.py` runs the bot

---
## disclaimer 
* after running the previous command, you should then invite the bot to your server, so that when the bot joins the server the prefix is assigned 
* default prefix is `£`

---
## credits 
* https://thedogapi.com/ and https://thecatapi.com/ for animal pictures 
* https://github.com/gentutu/bestbot for code (checking for files, cat and dog API calls)
* https://github.com/Rapptz/discord.py for the discord.py API wrapper

---
## license 
licensed under the GPLv3: http://www.gnu.org/licenses/gpl-3.0.html
