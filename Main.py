from TwitchBot import TwitchBot
import Settings

def main():

    username = Settings.username
    token = Settings.token
    client_id = Settings.client_id
    channel_limit = Settings.channel_limit

    print("Initializing Bot")
    # Initialize bot.
    bot = TwitchBot(username=username,
                    token=token,
                    client_id=client_id,
                    limit=channel_limit)

    # Runs the bot until user interrupts it.
    bot.run()


if __name__ == '__main__':
    main()
