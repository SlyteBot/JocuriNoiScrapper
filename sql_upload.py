from mysql.connector import connect, Error
from game import Game


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


    def insert_prdocuts

if __name__ == '__main__':
    instance = SQL()
    instance.extract_genres([])
