from mysql.connector import connect, Error


class SQL:
    def __init__(self):

        try:
            self.connection = connect(
                host="localhost",
                user="root",
                database="webshop"
            )
        except Error as e:
            print(e)

    def connection(self):
        return connect(
            host="localhost",
            user="root",
        )


if __name__ == '__main__':
    instance = SQL()
