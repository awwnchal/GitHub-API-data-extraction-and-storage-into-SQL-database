# GitHub-API-data-extraction-and-storage-into-SQL-database


# Description

This project extracts data from the GitHub API using a GET request and stores it in an SQL database. The data extracted is from the Apache Hadoop Github repository's contributors' endpoint. The first 100 contributors are extracted using the "per_page" variable in the API request.

The project is divided into five steps:

Familiarize with the GitHub API.

Extract JSON data corresponding to the first 100 contributors from the Apache Hadoop Github Repo's contributors endpoint using Java or Python.

Extract user information for each of the 100 contributors, such as login, id, location, email, hireable, bio, twitter_username, public_repos, public_gists, followers, following, and created_at.

Create an SQL database and table and store all the information obtained in step 3.

Optimize the SQL database for quick look-ups of "login", "location", and "hireable".

Dependencies

Python 3.0 or above,
Requests package,
SQLite package,

# Getting Started

Clone the repository to your local machine.

Open the project directory in a Python IDE of your choice.

Install the dependencies by running pip install -r requirements.txt in the terminal.

Run the code using python main.py in the terminal.

Check the created database file in the project directory.
