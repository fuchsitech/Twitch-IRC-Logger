FROM python:3.7-alpine


COPY Settings.py /data/Settomgs.py
COPY Main.py /run_bot.py
COPY TwitchBot.py /twitch_irc_bot.py
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

CMD [ "python3", "./run_bot.py" ]
