# Austen Rhyce Erickson
# Assignment 8.2

import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "movies_user",
    "password": "popcorn",
    "host": "127.0.0.1",
    "database": "movies",
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)
    print("\n Database user {} connected to MySql on host {} with database {}".format(config["user"], config["host"], config["database"]))
    mycursor = db.cursor()

    def show_films(cursor, title):
        cursor.execute("SELECT film_name AS name, film_director AS Director, genre_name AS Genre, studio_name AS 'Studio Name' FROM film INNER JOIN genre ON film.genre_id = genre.genre_id INNER JOIN studio ON film.studio_id = studio.studio_id")

        films = cursor.fetchall()

        print(f"\n  -- {title} --")

        for film in films:
            print(f"Film Name: {film[0]}\nDirector: {film[1]}\nGenre Name: {film[2]}\nStudio Name: {film[3]}\n")



    show_films(mycursor, "DISPLAYING FILMS")


except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("   The supplied username or password are invalid")
    
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("   The specified database does not exist")

    else:
        print(err)
    
finally:
    db.close()