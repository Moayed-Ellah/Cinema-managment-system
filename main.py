# project data
__version__ = "0.1.0"
__status__ = "Development"

# Generic/Built-in
from datetime import datetime
import pickle
import re
import sys

# global scope variables
user_data = "backend/authentication.dat"
session = 'backend/session.dat'
movies = 'backend/data.dat'
pending_tickets = 'backend/pending.dat'
accepted_tickets = 'backend/accepted.dat'
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


def login(username, password):
    """
    check if the user data has a match in the database

    :param username: username
    :type username: str
    :param password: password
    :type password: str
    :returns: True if login is successful, False otherwise
    """

    try:
        file = read(user_data, "rb")
        data = pickle.load(file)
        file.close()
    except EOFError:
        print("this file doesn't exist")

    if username in data:
        if data[username]["password"] == password:
            print("Login successful")
            return True
        else:
            print("Wrong password")
            return False
    else:
        print("Username not found")
        return False


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

    if not re.match("^[a-zA-Z0-9_]*$", username):
        print(
            "Username can only contain alphanumeric characters and underscores"
        )
    elif len(password) < 8:
        print("Password must be at least 8 characters long")
    elif not any(char.isdigit() for char in password):
        print("Password must contain at least one digit")
    elif not any(char.isupper() for char in password):
        print("Password must contain at least one uppercase letter")
    elif not any(char.islower() for char in password):
        print("Password must contain at least one lowercase letter")
    elif password != password_confirmation:
        print("Password and password confirmation do not match")
    else:
        try:
            file = read(user_data, "rb")
            data = pickle.load(file)
            file.close()
        except EOFError:
            print("this file doesn't exist")

        user_id = datetime.now().strftime('%Y%m%d%H%M%S')
        details = {
            "username": username,
            "id": user_id,
            "password": password,
            "password_confirmation": password_confirmation
        }

        data[username] = details

        file = read(user_data, "wb")
        pickle.dump(data, file)
        file.close()
        print("You've registered successfully")


# movies functions
def add(movie, description, price, seats):
    """
    adds a new movie to the collection of the data

    :param description: the details of the movie
    :type description: str
    :param seats: the number of available seats
    :type seats: int
    :param movie: the name of the movie to add
    :type movie: str
    :param price: the price of a ticket for the movie
    :type price: int
    """

    try:
        file = read(movies, "rb")
        data = pickle.load(file)
        file.close()
    except EOFError:
        print("this file doesn't exist")

    if movie in data:
        print("Movie already exists")
    else:
        data[movie] = {
            "description": description,
            "seats": seats,
            "price": price
        }

        file = read(movies, "wb")
        pickle.dump(data, file)
        file.close()
        print("Movie added successfully")


def delete(movie):
    """
    deletes a movie from the collection of the data

    :param movie: the name of the movie to delete
    :type movie: str
    """

    try:
        file = read(movies, "rb")
        data = pickle.load(file)
        file.close()
    except EOFError:
        print("this file doesn't exist")

    if movie in data:
        del data[movie]

        file = read(movies, "wb")
        pickle.dump(data, file)
        file.close()
        print("Movie deleted successfully")
    else:
        print("Movie does not exist")


def see_movies():
    """
    Lists all the available movies in the database.
    """
    try:
        file = read(movies, "rb")
        data = pickle.load(file)
        file.close()
    except EOFError:
        print("this file doesn't exist")

    if data:
        print("Here are the available movies:")
        for movie in data:
            print(f"- {movie}")
    else:
        print("There are no movies available.")


def list_customers(movie):
    """
    lists all customers who signed up for a specific film

    :param movie: the name of the movie
    :type movie: str
    """

    try:
        file = read(pending_tickets, "rb")
        data = pickle.load(file)
        file.close()
    except EOFError:
        print("this file doesn't exist")

    customers = []
    for customer in data:
        if data[customer]["movie"] == movie:
            customers.append(customer)

    if customers:
        print("Customers who signed up for", movie, ":")
        for customer in customers:
            print(customer)
    else:
        print("No customers signed up for", movie)


def list_movies():
    try:
        file = read(movies, "rb")
        data = pickle.load(file)
        file.close()
    except EOFError:
        data = {}
    if data:
        for movie in data:
            print(f"\nMovie: {movie}")
            print(f"Description: {data[movie]['description']}")
            print(f"Price: {data[movie]['price']}")
            print(f"Seats: {data[movie]['seats']}")
    else:
        print("No movies found.")


# tickets functions


def accept_booking(customer, movie):
    """
    accepts a booking request

    :param customer: the name of the customer
    :type customer: str
    :param movie: the name of the movie
    :type movie: str
    """

    try:
        file = read(pending_tickets, "rb")
        pending_data = pickle.load(file)
        file.close()
    except EOFError:
        print("this file doesn't exist")

    if customer in pending_data:
        if pending_data[customer]["movie"] == movie:
            try:
                file = read(accepted_tickets, "rb")
                accepted_data = pickle.load(file)
                file.close()
            except EOFError:
                print("this file doesn't exist")

            try:
                file = read(movies, "rb")
                data = pickle.load(file)
                file.close()
            except EOFError:
                print("this file doesn't exist")

            if movie not in data:
                print("Movie not found")
            else:
                accepted_data = {}
                accepted_data[customer] = {
                    "movie": movie,
                    "seats": pending_data[customer]["seats"],
                    "price": data[movie]["price"]
                }

                file = read(accepted_tickets, "wb")
                pickle.dump(accepted_data, file)
                file.close()

                del pending_data[customer]

                file = read(pending_tickets, "wb")
                pickle.dump(pending_data, file)
                file.close()
                print("Booking request accepted")
        else:
            print("Movie does not match booking request")
    else:
        print("Booking request not found")


def search(name):
    """
    Searches for a movie with the given name in the database.
    
    :param name: the name of the movie to search for
    :type name: str
    """
    try:
        file = read(movies, "rb")
        data = pickle.load(file)
        file.close()
    except EOFError:
        print("this file doesn't exist")

    if name in data:
        # Movie found
        movie = data[name]
        print(f"Movie found: {name}")
        print(f"Description: {movie['description']}")
        print(f"Price: {movie['price']}")
        print(f"Available seats: {movie['seats']}")
    else:
        # Movie not found
        print(f"Movie with name '{name}' not found.")


def send_book_request(customer, movie, seats):
    """
    sends a book request

    :param customer: the name of the customer
    :type customer: str
    :param movie: the name of the movie
    :type movie: str
    :param seats: the number of seats
    :type seats: int
    """

    try:
        file = read(movies, "rb")
        data = pickle.load(file)
        file.close()
    except EOFError:
        data = {}

    if movie not in data:
        print("Movie does not exist")
    else:
        if seats > data[movie]["seats"]:
            print("Not enough seats available")
        else:
            data[movie]["seats"] -= seats
            file = read(movies, "wb")
            pickle.dump(data, file)
            file.close()

            try:
                file = read(pending_tickets, "rb")
                pending_data = pickle.load(file)
                file.close()
            except EOFError:
                print("this file doesn't exist")
            pending_data = {}
            pending_data[customer] = {"movie": movie, "seats": seats}

            file = read(pending_tickets, "wb")
            pickle.dump(pending_data, file)
            file.close()
            print("Book request sent successfully")


def see_ticket(customer):
    """
    sees the movie ticket

    :param customer: the name of the customer
    :type customer: str
    """

    try:
        file = read(accepted_tickets, "rb")
        data = pickle.load(file)
        file.close()
    except EOFError:
        print("this file doesn't exist")

    if customer in data:
        ticket = data[customer]
        print("Movie:", ticket["movie"])
        print("Seats:", ticket["seats"])
        print("Price:", ticket["price"])
    else:
        print("Ticket not found")


def menu():
    print("\n - Cinema Ticketing System - \n")
    print("1. Customer")
    print("2. Vendor")
    print("0. Quit")
    choice = input("\nEnter your choice (0-2): ")
    return choice


while True:
    print("\n" + "-" * 50)
    choice = menu()
    if choice == "1":
        while True:
            print("\n" + "-" * 50)
            print("\n - Customer- \n")
            print("1. Login")
            print("2. Signup")
            print("0. Back")
            customer_choice = input("\nEnter your choice (0-2): ")

            if customer_choice == '1':
                print("\n - Log in - \n")
                username = input("Enter username: ")
                password = input("Enter password: ")
                if login(username, password):
                    while True:
                        print("\n" + "-" * 50)
                        print("\n - Customer Options - \n")
                        print("1. See movies")
                        print("2. Search for a movie")
                        print("3. Send book request")
                        print("4. See ticket")
                        print("0. Back")
                        customer_choice = input("\nEnter your choice (0-4): ")
                        if customer_choice == "1":
                            print("\n - See movies - \n")
                            see_movies()
                        elif customer_choice == "2":
                            print("\n - Search for a movie - \n")
                            search_term = input("Enter search term: ")
                            search(search_term)
                        elif customer_choice == "3":
                            print("\n - Send book request - \n")
                            customer = input("Enter customer name: ")
                            movie = input("Enter movie name: ")
                            seats = int(input("Enter number of seats: "))
                            send_book_request(customer, movie, seats)
                        elif customer_choice == "4":
                            print("\n - See ticket - \n")
                            customer = input("Enter customer name: ")
                            see_ticket(customer)
                        elif customer_choice == "0":
                            break
                        else:
                            print("Invalid choice")
            elif customer_choice == "2":
                print("\n - Sign up - \n")
                username = input("Enter username: ")
                password = input("Enter password: ")
                password_confirmation = input("Confirm password: ")
                signup(username, password, password_confirmation)
            elif customer_choice == "0":
                break
            else:
                print("Invalid choice")
    elif choice == "2":
        while True:
            print("\n" + "-" * 50)
            print("\n - Vendor Options - \n")
            print("1. Add movie")
            print("2. Delete movie")
            print("3. List movies")
            print("4. List customers for a movie")
            print("5. Accept a booking request")
            print("0. Back")
            vendor_choice = input("\nEnter your choice (0-5): ")
            if vendor_choice == "1":
                print("\n - Add movie - \n")
                movie = input("Enter movie name: ")
                description = input("Enter movie description: ")
                price = int(input("Enter ticket price: "))
                seats = int(input("Enter number of seats: "))
                add(movie, description, price, seats)
            elif vendor_choice == "2":
                print("\n - Delete movie - \n")
                movie = input("Enter movie name: ")
                delete(movie)
            elif vendor_choice == "3":
                print("\n - List movie - \n")
                list_movies()
            elif vendor_choice == "4":
                print("\n - List customers for a movie - \n")
                movie = input("Enter movie name: ")
                list_customers(movie)
            elif vendor_choice == "5":
                print("\n - Accept booking request - \n")
                customer = input("Enter customer name: ")
                movie = input("Enter movie name: ")
                accept_booking(customer, movie)
            elif vendor_choice == "0":
                break
            else:
                print("Invalid choice")
    elif choice == "0":
        break
    else:
        print("Invalid choice")
