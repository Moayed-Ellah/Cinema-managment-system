Cinema Management System
This code is for a cinema management system that allows customers to:

Register and login
View available movies
Search for specific movies
Send booking requests for tickets
It also allows vendors (such as cinema staff) to:

Login
Add or delete movies
View customers who have signed up for a specific film
Accept booking requests
Requirements
datetime
eel
pickle
re
Functions
Customers
login(user, password)
Check if the provided username and password match a user in the database. If the login is successful, it will create a session file to store the user's login status. If the login fails, it will set an alert message with an error message.
signup(username, password, password_confirmation)
Check if the provided username and password meet the minimum criteria for signing up (such as the username not already existing in the database and the password meeting certain length and complexity requirements). If the signup is successful, it will add the user's details to the database and set an alert message with a success message. If the signup fails, it will set an alert message with an error message.
see()
Display a list of all the movies in the database.
search(movie)
Search for a specific movie in the database. Returns a description of the movie if it is found.
send(movie, user, tickets)
Send a request for a ticket booking.
tickets(user)
View the customer's ticket requests. Returns a list of the customer's pending and accepted ticket requests.
Vendors
add(movie, description, price, seats)
Add a new movie to the collection of movies in the database. Updates the number of seats available for each movie.
delete(movie)
Remove a movie from the collection of movies in the database.
accept(movie, user)
Accept a ticket request. Updates the status of the ticket request to "accepted".
customers(movie)
View a list of all customers who have signed up for a specific movie. Returns a list of all the customers who have requested tickets for that movie.
Other
read(file, mode)
Open a file.
exists(user)
Check if a provided username exists in the database.
match(user, password)
Check if a provided password matches the password in the database for a given username.
search(movie)
Check if a provided movie name exists in the database.
