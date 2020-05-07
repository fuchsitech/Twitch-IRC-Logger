import psycopg2
import Settings

def psqlHandler():
    db = Settings.db
    try:
        connection = psycopg2.connect(user = db['user'],
                                      password = db['password'],
                                      host = db['host'],
                                      port = "5432",
                                      database = db['database'])

        #cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")

        # Print PostgreSQL version
        #cursor.execute("SELECT version();")
        #record = cursor.fetchone()
        #print("You are connected to - ", record,"\n")
        return connection


    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
#    finally:

        #closing database connection.
#            if(connection):
#                cursor.close()
#                connection.close()
#                print("PostgreSQL connection is closed")
