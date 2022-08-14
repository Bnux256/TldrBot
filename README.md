# TldrBot
A Discord bot client for the TLDR Pages -  a simpler alternative to man pages.
Gives you a comprehensible and informative reference manual for every command.
> "The name comes from the word TL;DR, which is an abbreviation for "too long; didn't read", referring to man pages that are said to be too long by several users." - Wikipedia
---
Run `/tldr tar` to get its TLDR manual: 
![Screenshot 2022-04-10 11 16 31 AM](https://user-images.githubusercontent.com/80382873/162609321-e9a24ba4-df22-4031-98a7-fcc733f6c14b.png)

## Try it out!:
DM the bot by searching `TldrBot#9162` in the `Find or start a conversation` tab in Discord.
Or [Click here to add the bot to your server!](https://discord.com/api/oauth2/authorize?client_id=930781398434992149&permissions=2048&scope=bot%20applications.commands)

## Installation 
### Docker-Compose: (recommended)
Clone the repo and add your bot token to the `docker-compose.yml` file or add a docker secret to it. 
Run `docker build . -t bnux256/tldrbot` to build the docker container.
Now to start the bot use: `docker compose up -d` and `docker compose stop` to stop it.

### Standalone (Instruction for UNIX os)- requires Python>=3.9:
Clone the repo and add your bot token to `.env` file. 
Create a venv using `python3 -m venv venv` and enter into it using `source venv/bin/activate`.
Install dependencies by running `pip3 install -r requirments.txt`
Now to start it (if you are already inside the venv you created) run `python3 main.py`.