from flask import Flask,render_template

app = Flask(__name__)

import config
import routes
from models import db, User, company, drive, candidate, candidate_drive

if __name__ == '__main__':
    app.run(debug=True)

