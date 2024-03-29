from dotenv import load_dotenv
from os import getenv
from get_links import Links
from sql_upload import SQL, Error
# .env file
# HOST="HOST"
# USERNAME="USERNAME"
# DATABASE="DATABASE"
# PASSWORD="PASSWORD"


def sql_test_connection(host, user, database, password):
    try:
        instance = SQL(host, user, database, password).connection()
    except Error as e:
        print("error")


def main():
    load_dotenv()

    host = getenv("HOST")
    user = getenv("USERNAMEDB")
    database = getenv("DATABASE")
    password = getenv("PASSWORD")

    filename = "links.txt"
    links = []
    SQL_instance = SQL(host, user, database, password)

    try:
        SQL_instance.connection()
        print("SQL Server connection successful!")
    except Error as e:
        print("Connection to server failed.")
        return

    with open(filename, mode="r") as f:
        for link in f:
            links.append(link.strip())

    link_instance = Links(links, SQLconnection=SQL_instance, number_of_pages=3)
    link_instance.threading_games()


if __name__ == "__main__":
    main()
