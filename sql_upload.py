from mysql.connector import connect, Error
from game import Game
import datetime


class SQL:

    def __init__(self, host: str, user: str, database: str, password: str) -> None:
        self.host = host
        self.user = user
        self.database = database
        self.password = password

    def connection(self):
        try:
            connection = connect(
                host=self.host,
                password=self.password,
                user=self.user,
                database=self.database
            )
            return connection
        except Error as err:
            raise err

    def extract_genres(self, games: [Game]):
        with self.connection() as connection:
            cursor = connection.cursor()
            select_genres = ("SELECT genre_name FROM `genres`")

            cursor.execute(select_genres)
            genres_exist = []
            genres = []
            for genre_name in cursor:
                genres_exist.append(genre_name[0].strip())
            genres = []
            for game in games:
                for genre in game.genres:
                    value = genre.strip()
                    if value not in genres_exist and value not in genres:
                        genres.append(value)
            add_genre = ("INSERT INTO genres"
                         "(genre_name)"
                         "VALUES (%s);")

            for genre in genres:
                cursor.execute(add_genre, [genre])
            connection.commit()
            cursor.close()

    def insert_prodcuts(self, games: [Game]):

        with self.connection() as connection:
            cursor = connection.cursor()
            get_platforms = ("SELECT platform_name, ID FROM `platforms`; ")
            get_genres = ("SELECT genre_name, ID FROM `genres`; ")
            cursor.execute(get_platforms)
            platforms = {}
            for platform_name, ID in cursor:
                platforms[platform_name] = ID

            cursor.execute(get_genres)
            genres = {}
            for genre_name, ID in cursor:
                genres[genre_name] = ID

            add_product = ("INSERT INTO products"
                           "(product_name_id,product_name,product_date,product_price,product_publisher,product_developer,ID_platform)"
                           "VALUES (%s,%s,%s,%s,%s,%s,%s);")
            add_product_genre = ("INSERT INTO products_genres"
                                 "(ID_product,ID_genre)"
                                 "VALUES (%s,%s);"
                                 )
            for game in games:
                date_split = game.date.split('-')
                try:
                    product_data = (game.id_name, game.name, datetime.date(
                        int(date_split[0]), int(date_split[1]), int(date_split[2])), game.price, game.publisher, game.developer, platforms[game.platform])
                    cursor.execute(add_product, product_data)
                    connection.commit()

                    product_id = cursor.lastrowid

                    for genre in game.genres:
                        product_genre_data = (product_id, genres[genre])
                        cursor.execute(add_product_genre, product_genre_data)
                        connection.commit()
                except KeyError as e:
                    pass
            connection.commit()
            cursor.close()
