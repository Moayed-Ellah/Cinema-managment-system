<h1>
            Cinema Management System
          </h1>
          <p>
            This code is for a cinema management system that allows customers to:
          </p>
          <ul>
            <li>
              Register and login
            </li>
            <li>
              View available movies
            </li>
            <li>
              Search for specific movies
            </li>
            <li>
              Send booking requests for tickets
            </li>
          </ul>
          <p>
            It also allows vendors (such as cinema staff) to:
          </p>
          <ul>
            <li>
              Login
            </li>
            <li>
              Add or delete movies
            </li>
            <li>
              View customers who have signed up for a specific film
            </li>
            <li>
              Accept booking requests
            </li>
          </ul>
          <h2>
            Requirements
          </h2>
          <ul>
            <li>
              <code>datetime</code>
            </li>
            <li>
              <code>eel</code>
            </li>
            <li>
              <code>pickle</code>
            </li>
            <li>
              <code>re</code>
            </li>
          </ul>
          <h2>
            Functions
          </h2>
          <h3>
            Customers
          </h3>
          <ul>
            <li>
              <code>login(user, password)</code>
              <br>
              Check if the provided username and password match a user in the database. If the login is successful, it will create a session file to store the user's login status. If the login fails, it will set an alert message with an error message.
            </li>
            <li>
              <code>signup(username, password, password_confirmation)</code>
              <br>
              Check if the provided username and password meet the minimum criteria for signing up (such as the username not already existing in the database and the password meeting certain length and complexity requirements). If the signup is successful, it will add the user's details to the database and set an alert message with a success message. If the signup fails, it will set an alert message with an error message.
            </li>
            <li>
              <code>see()</code>
              <br>
              Display a list of all the movies in the database.
            </li>
            <li>
              <code>search(movie)</code>
              <br>
              Search for a specific movie in the database. Returns a description of the movie if it is found.
            </li>
            <li>
              <code>send(movie, user, tickets) </code>
              <br>
              Send a request for a ticket booking.
            </li>
            <li>
              <code>tickets(user)</code>
              <br>
              View the customer's ticket requests. Returns a list of the customer's pending and accepted ticket requests.
            </li>
          </ul>
          <h3>
            Vendors
          </h3>
          <ul>
            <li>
              <code>add(movie, description, price, seats) </code>
              <br>
              Add a new movie to the collection of movies in the database. Updates the number of seats available for each movie.
            </li>
            <li>
              <code>delete(movie)</code>
              <br>
              Remove a movie from the collection of movies in the database.
            </li>
            <li>
              <code>accept(movie, user)</code>
              <br>
              Accept a ticket request. Updates the status of the ticket request to "accepted".
            </li>
            <li>
              <code>customers(movie)</code>
              <br>
              View a list of all customers who have signed up for a specific movie. Returns a list of all the customers who have requested tickets for that movie.
            </li>
          </ul>
          <h3>
            Other
          </h3>
          <ul>
            <li>
              <code>read(file, mode)</code>
              <br>
              Open a file.
            </li>
            <li>
              <code>exists(user)</code>
              <br>
              Check if a provided username exists in the database.
            </li>
            <li>
              <code>match(user, password)</code>
              <br>
              Check if a provided password matches the password in the database for a given username.
            </li>
            <li>
              <code>search(movie)</code>
              <br>
              Check if a provided movie name exists in the database.
            </li>
            <li>
            </li>
          </ul>
        </div>
      </div>
    </div>
