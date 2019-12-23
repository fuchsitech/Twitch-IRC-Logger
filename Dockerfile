FROM python:3.7-alpine


COPY Channels.py /data/Channels.py
COPY config.ini /data/config.ini
COPY run_bot.py /run_bot.py
COPY twitch_irc_bot.py /twitch_irc_bot.py
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

CMD [ "python3", "./run_bot.py" ]
