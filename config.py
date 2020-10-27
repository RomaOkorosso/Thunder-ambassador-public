import psycopg2

main = ''
roman = 1111

host = ''
database = ''
user = ''
port = '5432'
password = ''


def connect_with_database():
    con = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return con
