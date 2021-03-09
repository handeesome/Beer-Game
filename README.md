# se-01-team-31

SE Sprint 01, Team 31

## Overview

The submission contains the login pages for the Beer Distribution game implemented with HTML/CSS for front-end as well as a database for the instructor login implemented with Django and MySQL.
 
 The index page allows you to choose a log in option as Instructor, Student or to create a custom game.

## Requirements

## Structure

The *templates* folder contains the HTML files and the *static* folder contains the CSS. 

The *SE* folder contains the Django files to save the Instructor sign up data i.e, the name, e-mail and password into a MySQL database.

* [models.py](SE/models.py) saves the data into the database
* [views.py](SE/views.py) connects to the database and renders the HTML files.

### Changes to the original requirements document

One of the requirements that Professor Chankov mentioned was for students to be able to create their own game. This requirement was missing in the original document. 

We added the [signup-costum.html](template/signup-costum.html) and the [custom_login.html](template/custom_login.html) file to allow students to either sign up or log in (if they already have credentials) and make a custom game.
