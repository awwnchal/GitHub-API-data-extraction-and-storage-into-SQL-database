import requests
import mysql.connector
import warnings
import json


## Question 2: Extract the JSON corresponding to the first 100 contributors from this API. 
##  https://api.github.com/repos/apache/hadoop/contributors

url = "https://api.github.com/repos/apache/hadoop/contributors"
headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0', 'Authorization': 'token ' + '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'}  ## Enter 'token [code]'
#headers = {'Authorization': 'token' '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'}  
params = {"per_page": 100}

response = requests.get(url, params=params, headers=headers)
contributors = response.json()
print(contributors)


## Question 3: For each of the 100 contributors extracted in (2), write code that accesses their user information and 
## extracts "login", "id", "location", "email", "hireable", "bio", "twitter_username", "public_repos", "public_gists",
## "followers", "following", "created_at".

all_user_information_list = []
for contributor in contributors:
        user_url = contributor["url"]
        user_response = requests.get(user_url, headers=headers)
        user_information = user_response.json()
        
        ## extracts "login", "id", "location", "email", "hireable", "bio", "twitter_username", 
        ## "public_repos", "public_gists", "followers", "following", "created_at"
        login = user_information["login"]
        user_id = user_information["id"]
        location = user_information["location"]
        email = user_information["email"]
        hireable = user_information["hireable"]
        bio = user_information["bio"]
        twitter_username = user_information["twitter_username"]
        public_repos = user_information["public_repos"]
        public_gists = user_information["public_gists"]
        followers = user_information["followers"]
        following = user_information["following"]
        created_at = user_information["created_at"]
        ## store each user information into a list for question (4)
        user_information_list = [login,user_id, location, email, hireable, bio, twitter_username, public_repos, public_gists, followers, following, created_at]
        ## store all lists into a list
        all_user_information_list.append(user_information_list)


        print(f"Login: {login}")
        print(f"Id: {user_id}")
        print(f"Location: {location}")
        print(f"Email: {email}")
        print(f"Hireable: {hireable}")
        print(f"Bio: {bio}")
        print(f"Twitter Username: {twitter_username}")
        print(f"Public Repos: {public_repos}")
        print(f"Public Gists: {public_gists}")
        print(f"Followers: {followers}")
        print(f"Following: {following}")
        print(f"Created at: {created_at}")
        print()



## Question 4. Write code that creates an SQL database + table, and stores all the information obtained in (3) in it.  
## Please be cautious of the data type you choose for each collumn and briefly justify your decisions.  What do you choose as Primary Key and why?

#ignore warnings
warnings.filterwarnings("ignore")
SQL_DB = "API_database"

###### Answers for choosing data type for each column:
## I chose Id as primary key because "Id" is unique for each user and it is unlikely to change over time, which can be used as a reliable identifier for each row in the databse.
## Data type for Login, Location, Email, Hireable, Twitter_Username and Created_at: VARCHAR(100), because these columns contains strings and 100 provides a reasonable maximum length to store the data.
## Data type for Bio: VARCHAR(1000), because because these columns contains longer strings and 1000 provides a reasonable maximum length to store the data.
## Data type for Public_Repos, Public_Gists, Followers, Following: INTEGER, because these columns contains a whole numbers without decimal points.


def main():
    
    SQL_TABLE_API = "API"
    SQL_TABLE_API_DEF = "(" + \
            "Id INTEGER PRIMARY KEY" + \
            ",Login VARCHAR(100)" + \
            ",Location VARCHAR(100)" + \
            ",Email VARCHAR(100)" + \
            ",Hireable VARCHAR(100)" + \
            ",Bio VARCHAR(1000)" + \
            ",Twitter_Username VARCHAR(100)" + \
            ",Public_Repos INTEGER" + \
            ",Public_Gists INTEGER" + \
            ",Followers INTEGER" + \
            ",Following INTEGER" + \
            ",Created_at VARCHAR(100)" + \
            ")"

    create_sql_table(SQL_TABLE_API, SQL_TABLE_API_DEF)
    
    try:
        #connect to server
        conn = mysql.connector.connect(host='localhost',
                                            database='API_database',
                                            user='root',
                                            password='mysql')  ## Enter MySQL password

        cursor = conn.cursor()


        #parametrized version
        parameterized_stmt = "INSERT INTO " + SQL_TABLE_API + " (Login, Id, Location, Email, Hireable, Bio, Twitter_Username, Public_Repos, Public_Gists, Followers, Following, Created_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"


        for el in all_user_information_list:
            #parameterized version
            cursor.execute(parameterized_stmt, (el))

        conn.commit()
        cursor.close()
        conn.close()

    except IOError as e:
        print(e)

   
def create_sql_table(SQL_TABLE_API, SQL_TABLE_API_DEF):
    try:
        
        #connect to server
        conn = mysql.connector.connect(host='localhost',
                                            user='root',
                                            password='mysql')   ## Enter MySQL password
        cursor = conn.cursor()

        query = "CREATE DATABASE IF NOT EXISTS " + SQL_DB
        print(query)
        cursor.execute(query);
        
        query = "CREATE TABLE IF NOT EXISTS " + SQL_DB + "." + SQL_TABLE_API + " " + SQL_TABLE_API_DEF + ";";
        print(query)
        cursor.execute(query);
        cursor.close()
        conn.close()
        return

    except IOError as e:
        print(e)


if __name__ == "__main__":
    main()



## Question 5. Optimize your code in (4) to allow for quick look-ups of "login", "location", and "hireable".  
## I.e., I would like, for example, to run the command  <<  SELECT * FROM table WHERE location = "Tokyo"  >>  fast.  What choices do you make and why?


## Answer: I chose to create index on the "login", "location", and "hireable" columns because creating index can help quickly find the rows that match 
## the WHERE clause without having to scan the entire table. 
# Create an index to optimize the code in (4):
# cursor.execute('CREATE INDEX index_login ON SQL_TABLE_API (login)')
# cursor.execute('CREATE INDEX index_location ON SQL_TABLE_API (location)')
# cursor.execute('CREATE INDEX index_hireable ON SQL_TABLE_API (hireable)')


###### Modified code #######

#ignore warnings
warnings.filterwarnings("ignore")
SQL_DB = "API_database"


def main():
    
    
    try:
        #connect to server
        conn = mysql.connector.connect(host='localhost',
                                            database='API_database',
                                            user='root',
                                            password='mysql')   ## Enter MySQL password

        cursor = conn.cursor()

       
        # Create an index to optimize the code in (4):
        cursor.execute('CREATE INDEX index_login ON API (login)')
        cursor.execute('CREATE INDEX index_location ON API (location)')
        cursor.execute('CREATE INDEX index_hireable ON API (hireable)')


        conn.commit()
        cursor.close()
        conn.close()

    except IOError as e:
        print(e)



if __name__ == "__main__":
    main()
