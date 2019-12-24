import psycopg2
import logging
import time
import Settings

class psqlHandler(logging.Handler):

    initial_sql = """CREATE TABLE IF NOT EXISTS log(
                        msg_id int,
                        channel text,
                        user text,
                        message text,
                        timestamp text
                   )"""

    insertion_sql = """INSERT INTO log(
                            msg_id,
                            channel,
                            user,
                            message,
                            timestamp)
                            VALUES (
                            %(msg_id)s,
                            %(channel)s,
                            %(user)s,
                            %(message)s,
                            %(timestamp)s
                    )"""

    def connect(self):
        try:
            self.__connect = psycopg2.connect(
                database=self.__database,
                host=self.__host,
                user=self.__user,
                password=self.__password,
                sslmode="disable")

            return True
        except:
            return False

    def __init__(self):
        db = Settings.db

        self.__database = db['database']
        self.__host = db['host']
        self.__user = db['user']
        self.__password = db['password']

        self.__connect = None

        if not self.connect():
            raise ConnectionError

        logging.Handler.__init__(self)

        self.__connect.cursor().execute(psqlHandler.initial_sql)
        self.__connect.commit()
        self.__connect.cursor().close()

    def emit(self, record):

        # Use default formatting:
        self.format(record)

        if record.exc_info:
            record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
        else:
            record.exc_text = ""

        # Insert log record:
        try:
            cur = self.__connect.cursor()
        except:
            self.connect()
            cur = self.__connect.cursor()

        cur.execute(psqlHandler.insertion_sql, record.__dict__)

        self.__connect.commit()
        self.__connect.cursor().close()
