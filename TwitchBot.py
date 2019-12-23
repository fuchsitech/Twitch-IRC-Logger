import socket
import time
from codecs import decode
import os
import Settings
import logging
import logging.handlers

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)

# Set our logger's time format to UTC
logging.Formatter.converter = time.gmtime

# Where logs will be stored.
logs_folder = os.path.join(os.getcwd(), 'logs/')

# Make the folder if it does not exist.
if not os.path.exists(logs_folder):
    os.mkdir(logs_folder)

# Set up the logger. Log files will rotated saved every 10 minutes.
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s — %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.handlers.TimedRotatingFileHandler(logs_folder + 'chat.log',   # Active log name
                                                                        when='M',
                                                                        interval=10,  # Log rotation in min.
                                                                        encoding='utf-8')])

class TwitchBot(object):
    """
    A bot which joins multiple Twitch IRC channels and records
    their messages to a rotating log file. The channels it joins
    are from a list of the streams with the most current viewers
    retrieved from the Twitch API. The number of streams to log
    can be configured up to a max. of 100.
    """

    def __init__(self, username, token, client_id, game='', refresh_interval=60, limit=25):
        """
        Initializes TwitchBot

        :param username:    What the bot will call itself when joining the IRC server. Do not use the same
                            name as a popular streamer, it will break the script.
        :param token:       The OAuth token used to join the Twitch IRC.
        :param client_id:   The client_id of your Twitch dev. application. See: https://dev.twitch.tv/docs/v5
        :param game:        The game that you want all streams to be playing. e.g. 'Overwatch'. Default: Any game ('').
        :param refresh_interval: How often (in seconds) to call __update() and get a new list of top streams. Default: 60
        :param limit:       The maximum numbers of streams to join. Default: 25 Max: 100
        """

        self.__server = 'irc.chat.twitch.tv'  # Twitch IRC IP Address
        self.__port = 6667                    # Twitch IRC Port
        self.username = username
        self.token = token
        self.client_id = client_id

        self.refresh_interval = refresh_interval
        self.game = game
        self.limit = limit

        # Get an initial list of streams.
        self.channel_list = Channels.channels

        # Connect to the Twitch IRC.
        self.__connect()

    def __connect(self):
        """
        Connect to the twitch.tv IRC server and then JOIN each IRC channel in self.channel_list

        :return: None
        """

        self.sock_connection = socket.socket()
        self.sock_connection.connect((self.__server, self.__port))

        self.sock_connection.send('PASS {}\n'.format(self.token).encode('utf-8'))
        self.sock_connection.send('NICK {}\n'.format(self.username).encode('utf-8'))

        # Call __join_channel() for all channels in the channel_list
        for channel in self.channel_list:

            self.__join_channel(channel)

    def __join_channel(self, channel):
        """
        Joins the specified twitch.tv IRC channel
        :param channel: The twitch.tv IRC channel to join. Usually (always?) the caster's channel name.

        :return: None
        """

        self.sock_connection.send('JOIN #{}\n'.format(channel).encode('utf-8'))

    def __leave_channel(self, channel):
        """
        Leaves the specified twitch.tv IRC channel
        :param channel: The twitch.tv IRC channel to leave. Usually (always?) the caster's channel name.

        :return: None
        """

        self.sock_connection.send('PART {}\n'.format(channel).encode('utf-8'))

    def __close_connection(self):
        """
        Close our socket connection.

        :return:
        """
        print('Exiting...')

        self.sock_connection.close()

        exit(0)

    def __log_message(self, response):
        """
        Save a valid message to your logs. A valid message is one that is
        NOT a PING from the server, IS greater than 0 in length, and
        does NOT contain our own name (such as those from the IRC
        server when we first join). Choosing the same *username* for
        the bot as a popular streamer will probably (100%) break the
        logging for said streamer's channel at best. I have no idea
        what a worst-case-scenario would be (disabled for 'impersonation'?).
        Investigate at your own discretion.

        :param response: A single message response from the server.
        :return:
        """
        # Send a PONG if the server sends a PING
        if response.startswith('PING'):

            self.sock_connection.send('PONG\n'.encode('utf-8'))

        elif len(response) > 0 and self.username not in response and not response.startswith(":tmi.twitch.tv"):

            logging.info(response.rstrip('\r\r\n'))

    def run(self):
        """
        Run the script until user interruption.

        :return: None
        """

        # A flag used to determine if it'stime to call __update().

        while True:

            try:

                # Get response from the IRC server
                try:

                    response = decode(self.sock_connection.recv(2048), encoding='utf-8')

                except UnicodeDecodeError:
                    # TODO Handle this better
                    # Sometimes this exception is raised, however it happens extremely
                    # rarely (< ~0.1%) and is not significant unless it is absolutely critical
                    # you do not miss anything. At the moment we simply skip over these errors.
                    continue

                # Sometimes in a busy channel many messages are received
                # in one 'response' and we need to split them apart. See
                # https://stackoverflow.com/q/28859961 for a longer and
                # more detailed explanation by someone else with the
                # same issue.
                #
                # All message end with '\r\n' so we can reliably count/split
                # them this way.

                line_count = response.count("\r\n")
                if line_count > 1:

                    messages = response.split("\r\n")

                    for single_msg in messages:

                        self.__log_message(single_msg)

                else:

                    self.__log_message(response)

            # Shut down 'gracefully' on keyboard interrupt.
            except KeyboardInterrupt:

                self.__close_connection()
