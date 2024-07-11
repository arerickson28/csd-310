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

#   INSERTING
    insert_into_genre_query = "INSERT INTO genre (genre_name) VALUES ('SciFi Drama')"
    mycursor.execute(insert_into_genre_query)
    # db.commit()
    select_genre_sub_query = "SELECT genre_id FROM genre WHERE genre_name = 'SciFi Drama'"

    insert_into_studio_query = "INSERT INTO studio (studio_name) VALUES ('FilmNation Entertainment')"
    mycursor.execute(insert_into_studio_query)
    # db.commit()
    select_studio_sub_query = "SELECT studio_id FROM studio WHERE studio_name = 'FilmNation Entertainment'"

    insert_into_film_query = f"INSERT INTO film (film_name, film_releaseDate, film_runtime,film_director, genre_id, studio_id) VALUES ('Arrival', '2016', '116', 'Denis Villeneuve', ({select_genre_sub_query}), ({select_studio_sub_query}))"
    mycursor.execute(insert_into_film_query)
    # db.commit()

    show_films(mycursor, "DISPLAYING FILMS AFTER INSERT")

#   UPDATING
    select_horror_sub_query = "SELECT genre_id FROM genre WHERE genre_name = 'Horror'"
    update_query = f"UPDATE film SET genre_id = ({select_horror_sub_query}) WHERE film_name = 'Alien'"
    mycursor.execute(update_query)

    show_films(mycursor, "DISPLAYING FILMS AFTER UPDATE - Changed Alien to Horror")

#   DELETING
    delete_query = "DELETE FROM film WHERE film_name = 'Gladiator'"
    mycursor.execute(delete_query)

    show_films(mycursor, "DISPLAYING FILMS AFTER DELETE")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("   The supplied username or password are invalid")
    
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("   The specified database does not exist")

    else:
        print(err)
    
finally:
    db.close()
