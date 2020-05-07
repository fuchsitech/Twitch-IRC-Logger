# -*- coding: utf-8 -*-
from TwitchBot import TwitchBot
import Settings

def main():
    bot_account = Settings.bot

    username = bot_account["username"]
    token = bot_account["token"]
    client_id = bot_account["client_id"]
    channel_limit = bot_account["channel_limit"]

    # Initialize bot.
    bot = TwitchBot(username=username,
                    token=token,
                    client_id=client_id,
                    limit=channel_limit)

    # Runs the bot until user interrupts it.
    bot.run()


if __name__ == '__main__':
    main()
