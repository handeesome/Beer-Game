# se-02-team-31
SE Sprint 02, Team 31  
March 10th, 2021


# Note
Our group has proposed some changes to the specification. It can be found in bonus.txt in the root folder. These changes made the implementation a lot easier, and we think they can also be very helpful for others.

## Table of contents
* [General info](#general-info)
* [Description](#description)
* [Setup](#setup)


# General info:
* **Frontend:** HTML, CSS, JS, Bootstrap  
* **Backend:** Python, Django

For this sprint, our team has basically implemented everything required on the specification (there is of course room for improvement). The previous group had only created some models of the database. This app is deployed on the CLAMV server, but due to the lack of dependencies installed there, it does not work. Information regarding the functionalities implemented can be found in the description.



# Description
### What we have implemented in XP2:
* User (instructor/student) can register, login. Authentication and authorization implemented.
* User (instructor/student) can create and start games, by specifying the roles, the players, and other settings of the games.
* User (instructor/student) can delete, and update games (even while the game is being played)
* Student can play more than one game. For each game, every information needed is displayed (plots, tables, orders from other players). The main logic of the game is implemented.
* Each user (student/instructor) can view a list of the games he/she has created and those he/she is playing.
* The admin of the game can monitor the game (view plots, total cost etc.)
* At the end of the game, each user can view the game statistics ( all the plots, tables).

### Project Structure
This Django project contains only one app, which is called 'game'.

##### File Structure
```
../                                 # project directory
    game/                           # main project default app
        __pycache__/
        migrations/ ...             # storing all the migrations
        static/game/
            img/ ...                # images
            game-view-style.css     
            style.css
        templates/game/             # containing all html files
            *html files
        views/                      # views implemented as a python module
            __pycache__
            __init__.py
            crudGame.py             # create, delete, update game
            enterGame.py            # backend func. related to game playing
            monitorGame.py          # game monitoring
            userview.py             # login, sigunp, logout, list of games
        admin.py                    # admin page
        apps.py
        forms.py                    # forms needed for the implementation
        models.py                   # all db models
        tests.py        
        urls.py
    mysite/                         # container of the whole project
        __pycache__/ ...             
        __init__.py               
        asgi.py
        settings.py
        urls.py
        wsgi.py
    bonus.txt                       # some changes to the original specs
    db_model_django.txt             # explanations regarding the db
    manage.py
    README.md
    
```



# Setup
1. Clone this repository
```
git clone https://github.com/lorenzorota/se-02-team-31.git
```
2. Install **MySQl** (if not currently installed)
3. Create a virtual environment and activate it. More information regarding that can be found [here](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)
4. All the dependencies of this project can be found in requirements.txt file. In order to install them just run the command:
```
pip install -r requirements.txt
```
If one of the dependencies cannot be installed, try to install them with pip.\
Note: More information installing **mysql-client** (Windows/Linux) if the above command did not work can be found [here](https://medium.com/@omaraamir19966/connect-django-with-mysql-database-f946d0f6f9e3).

5. After installation create a new database on Mysql, and include the information regarding it in /mysite/settings.py in the DATABASES section. More information can be found in the link given above.

6. Make migrations (construction of the database)
```
python manage.py makemigrations
python manage.py migrate

```
7. Run the server
```
python manage.py runserver

```
8. Navigate to http://localhost:8000/ and enjoy the game!

For a better testing of the game:
- Create 5 users (4 students, 1 instructor), signup, login
- Login in with the instructor and create some games (more than 1), including the students you created, having different options (wholesaler, distributor present/not present). Recommended: Nr of weeks should not be too large, and information delay should be small (to notice the game logic better)
- Start the games, at the main page, by clicking the link start game.
- For testing purposes, each round lasts only 5 minutes. These can be changed at /views/crudGame.py. You have a variable at top, called round_length. If you want hours, days,weeks, instead of minutes you can change that at *startGame* view found in the same file.
- Login in with the users created and play all the games concurrently. Do that for all the users (keep in mind the 5 minute length of the round).
- You can notice that the logic of the game is implemented (order placed by a role, becomes a demand to another one, outgoing shipment becomes incoming shipment to the other role of the same game)
- You can view the plots, the tables, or monitor the game (through the admin of the game).

