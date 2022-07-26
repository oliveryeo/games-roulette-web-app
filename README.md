# Games Roulette
#### Video Demo:
https://www.youtube.com/watch?v=BZUR2kbreqw
#### Description:
With the COVID-19 Pandemic, more and more people will be home-bound and I'm sure most of them would like to spend their time playing video games. But where do we start? What games do we play? This is the most common question we ask ourselves when we do not have a game in mind. This is where Games Roulette come into play, to potentially collate all different games with the help of the users as well. If you have no idea what games to play, the games roulette has a roulette picker which randomize and chooses a game for you!

**Framework used: Flask**

**Database used: SQLite**

Most of the design is taken from bootstrap.

**Functions of the web app:**
    Users can view recently added games in the homepage of the web app. Users can also request games to be added onto the web app database that they are passionate about.
    There is an administrator user in the database which is used to approve user's games requests. This is to avoid the users from typing in gibberish and registering it into the games database. However, to 'admin' the user, you will have to go into the database and edit accordingly.
    There are also different genre categories users can choose from in the web app to view specific kinds of game genres they want to see.
    There are also a roulette function in the web app which helps users to select any kind of game by randomisation. This is used when the user have no idea what games they want to play!
    And as usual, there is a log in and log out function in the web app. However, newly registered users are obviously not 'admined' upon registration.

Templates:
    1. The action.html, adventure.html, roleplaying.html, simulation.html, sports.html and strategy.html are all used to display the different categories of different games. Application.py will handle different data display from the database to fit in these html pages.
    2. Admin.html shows the approval page for admins to approve games requests and distinguish between actual game request and gibberish game requests.
    3. Categories.html shows the different game genres the users can choose from to filter out specific game genres they want to see.
    4. Apology.html is used when there is an error in any of the web app process in the user's end
    5. Index.html shows the recently added games in the web app's database.
    6. Layout.html helps to ease the html creation of other files.
    7. Login and register.html helps users to log in and/or register themselves.
    8. Roulette.html displays the page where a random game is picked. Only when the button is clicked will the table display itself, choosing the specific game.

Static file:
    Static file contains the styles.css which is mostly used for styling the hyperlinks and navbar. This is mostly similar to pset9's finance!

Application.py shows at the back end, how information is handled after they are passed through the html forms.
