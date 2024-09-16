# Using Heroku to create a webapp

## Creating a Github repo

1. If you don't already have one, create a Github account at github.com
2. Create a new repository with the name of your webapp _This will be the home for your app. If you don't know how to use Github, read a tutorial or two._

#### This repo will need two special files: `procfile` and `requirements.txt`

1. Creating `procfile`
    1. Create a file named `procfile` (no extension) in the root directory of your repo
    2. This file will only have one line: `web: gunicorn app:app`

2. Creating `requirements.txt`
    1. Create a file named `requirements.txt` in the root directory of your repo
    2. On a computer with Python installed, use pip to install `gunicorn`, `flask`, `psycopg2`, and any other libraries you will need
    3. Run the command `pip freeze` and copy the output into `requirements.txt`. It should look something like this:
```
Click==7.0
Flask==1.1.1
gunicorn==19.9.0
...
```


## Deploying to Heroku
1. Create a Heroku account (or sign in) at heroku.com
2. We have two options here: we can either create a single app or a pipeline. For now we're just going to make a new app.
3. Click `New` > `Create a new app` and give it a name (this will also be the URL so keep it short and memorable)
4. Under deployment method, choose Github and follow the neccessary steps to connect your repo
5. Go to resources and add Heroku Postgres _this will be our database; you can follow any Python database tutorial to use it with the psycopg2 module_
6. Create a Flask app in your repo; it will auto deploy to Heroku and you can access it at `<appname>.herokuapp.com`
