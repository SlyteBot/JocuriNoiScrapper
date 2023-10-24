from dotenv import load_dotenv
from os import getenv
from get_links import Links
from sql_upload import SQL
# .env file
# HOST="HOST"
# USERNAME="USERNAME"
# DATABASE="DATABASE"
# PASSWORD="PASSWORD"


def main():
    load_dotenv()

    host = getenv("HOST")
    user = getenv("USERNAME")
    database = getenv("DATABASE")
    password = getenv("PASSWORD")

    filename = "links.txt"
    links = []

    with open(filename, mode="r") as f:
        for link in f:
            links.append(link.strip())

    link_instance = Links(links)
    games = link_instance.threading_games()

    SQL_instance = SQL(host, user, database, password)

    SQL_instance.extract_genres(games)
    SQL_instance.insert_prodcuts(games)


if __name__ == "__main__":
    main()
