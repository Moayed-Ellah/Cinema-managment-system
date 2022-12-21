"""
Cinema management system
    - Customer
        - register
            - login !
        - login
            - see movies
            - search for a movie
            - send book request !-
            - see the movie ticket !
    - Vendor
        - login
            - add a new movie or delete an old one !
            - list all customers who signed up for a specific film !
            - accept booking requests !
"""
# project data
__version__ = "0.1.0"
__status__ = "Development"

# Generic/Built-in
from datetime import datetime
import eel
import pickle
import re
import sys

# global scope variables
eel.init("./frontend")
user_data = "backend/database/users/authentication.dat"
session = 'backend/database/users/session.dat'
movies = 'backend/database/movies/data.dat'
pending_tickets = 'backend/database/tickets/pending.dat'
accepted_tickets = 'backend/database/tickets/accepted.dat'
alert = None


# system functions
def read(file, mode):
    """ Open a file. """

    try:
        the_file = open(file, mode)
    except IOError as e:
        print("Unable to open the file", file, "Ending program.\n", e)
        input("\n\nPress the enter key to exit.")
        sys.exit()
    else:
        return the_file


@eel.expose
def login(user, password):
    """
     check if the user data has a match in the database

     :param user: username
     :type user: str
     :param password: password
     :type password: str
     :returns: error on declined action
    """

    global alert
    if user == 'admin' and password == 'admin':
        alert = 'admin'
    elif not exists(user):
        alert = "! Username doesn't exist"
    elif not match(user, password):
        alert = "! Wrong password"
    else:
        try:
            current_session = read(session, "wb")
            pickle.dump(user, current_session)
            current_session.close()
            alert = 'user'

        except EOFError:
            current_session = read(session, "wb")
            pickle.dump(user, current_session)
            current_session.close()
            alert = 'user'
    return alert


@eel.expose
def signup(username, password, password_confirmation):
    """
     check if the user data meets the minimum criteria to signup

     :param username: username
     :type username: str
     :param password: password
     :type password: str
     :param password_confirmation: password confirmation
     :type password_confirmation: str
     :returns: alert message on error
    """

    global alert
    if search(username):
        if validate(password):
            if password == password_confirmation:
                try:
                    file = read(user_data, "rb")
                    data = pickle.load(file)
                    file.close()
                except EOFError:
                    data = {}
                user_id = datetime.now().strftime('%Y%m%d%H%M%S')
                details = ("username: ", username,
                           "\nid: ", user_id,
                           "\npassword: ", password,
                           "\npassword confirmation: ", password_confirmation, "\n")

                data[username] = details

                file = read(user_data, "wb")
                pickle.dump(data, file)
                file.close()
                alert = "! You've registered successfully"
            else:
                alert = "! Your password doesn't match"
    return alert


# movies functions
@eel.expose
def add(movie, description, price, seats):
    """
    adds a new movie to the collection of the data

    :param description: the details of the movie
    :type description: str
    :param seats: the number of available seats
    :type seats: int
    :param movie: the name of the movie to add
    :type movie: str
    :param price: the price of the entry
    :type price: int
    """

    try:
        file = read(movies, "rb")
        films = pickle.load(file)
        file.close()
    except EOFError:
        films = {}

    details = ("description: ", description,
               "\nprice: ", price,
               "\nseats: ", seats, "\n")

    films[movie] = details

    file = read(movies, "wb")
    pickle.dump(films, file)
    file.close()


@eel.expose
def remove(movie):
    """
    deletes the movie from the database

    :param movie: the name of the movie to delete
    :type movie: str
    :return: action notice
    """

    try:
        file = read(movies, "rb")
        films = pickle.load(file)
        file.close()
    except EOFError:
        print("! File is empty. You must add a film first before you can remove it.")

    try:
        del films[movie]
    except KeyError:
        print("! That film doesn't exist.")

    file = read(movies, "wb")
    pickle.dump(films, file)
    file.close()


@eel.expose
def find(movie):
    """
    searches for a movie in the file and return it if there's a match

    :param movie: movie name
    :type movie: str
    :return: movie name
    """

    try:
        file = read(movies, "rb")
        films = pickle.load(file)

        for key, value in sorted(films.items()):
            if key == movie:
                return True
        file.close()
        return False
    except EOFError:
        return "! File is empty."


@eel.expose
def list_movies():
    """
    lists all the movies in the system

    :return: a list of movies names that are in the database
    """

    try:
        file = read(movies, "rb")
        films = pickle.load(file)
        counter = 0
        names = []
        prices = []

        for key, value in sorted(films.items()):
            names.append(key)
            prices.append(value[3])
            counter += 1
        file.close()
        return counter, names, prices

    except EOFError:
        return "! File is empty."


# customer specific functions
@eel.expose
def book(movie):
    """
    allow the customer to book a ticket on a specific file

    :param movie: the movie name
    """
    if find(movie):
        try:
            file = read(pending_tickets, "rb")
            tickets = pickle.load(file)

            data = read(session, "rb")
            user = pickle.load(data)

            for _, value in sorted(tickets.items()):
                if value[3] == user and value[1] == movie:
                    return '-1'
            file.close()
        except EOFError:
            tickets = {}

        ticket_id = datetime.now().strftime('%Y%m%d%H%M%S')
        data = read(session, "rb")
        user = pickle.load(data)

        details = ("\nmovie: ", movie,
                   "user: ", user, "\n")

        tickets[ticket_id] = details

        file = read(pending_tickets, "wb")
        pickle.dump(tickets, file)
        file.close()
    else:
        return "this movie doesn't exist"


@eel.expose
def show_status(movie):
    try:
        file = read(pending_tickets, "rb")
        tickets = pickle.load(file)

        data = read(session, "rb")
        user = pickle.load(data)

        for key, value in sorted(tickets.items()):
            if value[3] == user and movie == value[2]:
                return key
        file.close()
    except EOFError:
        return "! file error"


@eel.expose
def show():
    try:
        file = read(pending_tickets, "rb")
        pending = pickle.load(file)
        ticket_id = []
        user = []
        movie_name = []

        for key, value in sorted(pending.items()):
            ticket_id.append(key)
            user.append(value[3].upper())
            movie_name.append(value[1])
        file.close()
        return ticket_id, user, movie_name
    except EOFError:
        return "! File is empty."


# validation functions
def validate(password):
    """
     checks for the password validity on a set of critic

     :param password: the text for checking the password
     :type password: str
     :returns: alert message of invalidity
    """

    global alert
    if len(password) < 6:
        alert = "! password should be at least six characters"
    elif not re.search("[A-Z]", password):
        alert = "! password should contain at least one capital letter"
    elif not re.search("[1-9]", password):
        alert = "! password should contain at least one number"
    elif re.search(' ', password):
        alert = "! password should not contain space"
    else:
        return True


def search(username):
    """
     search for the username in the database

     :param username: the text for indexing the search
     :type username: str
     :returns: alert message if not found
    """

    global alert
    admin = 'admin'
    if len(username) < 5:
        alert = "! username is too short"
    elif username == admin:
        alert = "! process prohibited!"
    elif exists(username):
        alert = "! username already exists"
    else:
        return True


def exists(username):
    """
    checks if the username already exists in the database

    :param username: for the search indexing
    :type username: str
    :return: boolean of weather the user exists
    """

    try:
        file = read(user_data, "rb")
        users = pickle.load(file)

        for key in sorted(users.keys()):
            if username == key:
                return True
        file.close()
        return False
    except EOFError:
        return False


def match(username, password):
    """
     loops through each line to check if the password matches the user

     :param username: username for search indexing
     :type username: str
     :param password: for an in depth search
     :type password: str
     :return: boolean value on match
    """

    try:
        file = read(user_data, "rb")
        users = pickle.load(file)

        for key, value in sorted(users.items()):
            if username == key:
                if value[5] == password:
                    return True

        file.close()
        return False
    except EOFError:
        return "! File is empty."


eel.start("signup.html", mode='brave', size=(800, 800))
