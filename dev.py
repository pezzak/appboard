#!flask/bin/python
from app import app
app.config['SQLALCHEMY_ECHO'] = True
app.run(debug = False, host='0.0.0.0')
