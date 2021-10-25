from flaskext.mysql import MySQL
from application import app

class Database:
  
    mysql = MySQL()
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = 'test'
    mysql = MySQL(app)
    #mysql.init_app(app)

    def __init__(self):
        pass

    def get_connection(self):
        return self.mysql