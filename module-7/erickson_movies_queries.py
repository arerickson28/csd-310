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

    genre_query = "SELECT * FROM genre"
    studio_query = "SELECT * FROM studio"
    sub_2h_movie_query = "SELECT film_name, film_runtime FROM film WHERE film_runtime < 120"
    films_alphabetical_by_director_query = "SELECT film_name, film_director FROM film ORDER By film_director ASC"

    def get_query_result(query):
        mycursor.execute(query)
        return mycursor.fetchall()

    studio_data = get_query_result(studio_query)
    genre_data = get_query_result(genre_query)
    sub_2h_movie_data = get_query_result(sub_2h_movie_query)
    films_by_alphabetical_director_data = get_query_result(films_alphabetical_by_director_query)

    def display_studio_data(studios):
        studio_records_message = "---- DISPLAYING Studio RECORDS --- \n"
        for studio in studios:
            studio_records_message += f'\nStudio ID: {studio[0]} \nStudio Name: {studio[1]} \n'
        studio_records_message += "\n"
        return studio_records_message

    def display_genre_data(genres):
        genre_records_message = "---- DISPLAYING Genre RECORDS --- \n"
        for genre in genres:
            genre_records_message += f'\nGenre ID: {genre[0]} \nGenre Name: {genre[1]} \n'
        genre_records_message += "\n"
        return genre_records_message
    
    def display_sub_2h_movie_data(sub_2h_movies):
        sub_2h_movies_records_message = "---- DISPLAYING Short Film RECORDS --- \n"
        for movie in sub_2h_movies:
            sub_2h_movies_records_message += f'\nMovie Name: {movie[0]} \nRuntime(min): {movie[1]} \n'
        sub_2h_movies_records_message += "\n"
        return sub_2h_movies_records_message
    
    def display_films_by_alphabetical_director_data(director_films):
        films_by_director_message = "---- DISPLAYING Director RECORDS in Order---\n"
        for film in director_films:
            films_by_director_message += f'\nFilm Name: {film[0]} \nDirector: {film[1]} \n'
        films_by_director_message += "\n"
        return films_by_director_message

    print(display_studio_data(studio_data))
    print(display_genre_data(genre_data))
    print(display_sub_2h_movie_data(sub_2h_movie_data))
    print(display_films_by_alphabetical_director_data(films_by_alphabetical_director_data))

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("   The supplied username or password are invalid")
    
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("   The specified database does not exist")

    else:
        print(err)
    
finally:
    db.close()