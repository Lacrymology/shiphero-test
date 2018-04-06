from flask import Flask

app = Flask('shiphero')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
