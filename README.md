# movie-tracker
A movie tracker application works with vlc extension  

running without docker:

**install mysql**

**create an instance folder**

**create a config.py inside instance folder with the following content:**

```
SECRET_KEY = '<yoursecretkey>'
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://<yourpassword>:<youruser>@{}/{}"\
    .format(os.getenv('MYSQL_HOST', 'localhost'), os.getenv('MYSQL_SCHEMA', 'test_db')) 
```

`pip install -r requirements.txt`

`python3 manage.py db init`
`python3 manage.py db migrate`
`python3 manage.py db upgrade`

`python3 manage.py runserver`

