from mysql.connector import connect, Error
from game import Game
import datetime


class SQL:

    def connection(self):
        try:
            return connect(
                host="localhost",
                user="root",
                database="webshop"
            )
        except Error as e:
            print(e)

    def extract_genres(self, games: list[Game]):
        genres = []
        for game in games:
            for genre in game.genres:
                if genre not in genres:
                    genres.append(genre)
        add_genre = ("INSERT INTO genres"
                     "(genre_name)"
                     "VALUES (%s);")
        with self.connection() as connection:
            cursor = connection.cursor()
            for genre in genres:
                cursor.execute(add_genre, [genre])
            connection.commit()
            cursor.close()

    def insert_prodcuts(self, games: list[Game]):

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
                product_data = (game.id_name, game.name, datetime.date(
                    int(date_split[0]), int(date_split[1]), int(date_split[2])), game.price, game.publisher, game.developer, platforms[game.platform])
                cursor.execute(add_product, product_data)
                connection.commit()

                product_id = cursor.lastrowid

                for genre in game.genres:
                    product_genre_data = (product_id, genres[genre])
                    cursor.execute(add_product_genre, product_genre_data)
                    connection.commit()

            connection.commit()
            cursor.close()


if __name__ == '__main__':
    instance = SQL()
    # instance.extract_genres([])
    instance.insert_prodcuts([Game("a", "a", "2020-09-28", 145.6,
                                   "publisher", "dev", "PS5", ["2D", "PLATFORMER"]), Game("b", "a", "2020-09-28", 145.6,
                                                                                          "publisher", "dev", "PS5", ["2D", "PLATFORMER"])])
