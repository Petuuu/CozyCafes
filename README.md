# Cozy Cafés
### *Find and review cozy cafés near you*


## Overview
**Cozy Cafés** is a web application built with **Python Flask** that helps users discover and review cozy cafés nearby.
Users can browse ratings, read reviews, and even contribute their own experiences.

## Features
- User Accounts - Users can create an account, log in, and manage their profile.
- Review Management - Add, edit, and delete café reviews easily.
- View Reviews - Browse all reviews shared by other users.
- Search Functionality - Find cafés or reviews using keywords.
- User Dashboard - Each user has a personal page showing their submitted reviews.
- Categories - Assign one or more categories or tags to each review (e.g., “Pet Friendly,” “Great Wi-Fi,” “Quiet Atmosphere”).
- Comments - Users can comment on reviews and interact with others.


## Installation guide

### Install Flask
Make sure you have Python installed, then install Flask using `pip`:
```
$ pip install flask
```

### Create the database
Initialize a new SQLite database using your schema file:
```
$ sqlite3 database.db < schema.sql
```

### Run the application:
Start the Flask development server:
```
$ flask run
```


## Handling large amounts of data
File `seed.py` add 1000 users, 100 000 reviews, and a million comments total. Before creating indexes to the database, changing pages on the home screen took from 0.7 to 0.9 seconds on average.
