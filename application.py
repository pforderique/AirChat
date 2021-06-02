from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from wtform_fields import *
from models import *

# configure app
app = Flask(__name__)
app.secret_key = 'replace later'

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

@app.route("/", methods = ["GET", "POST"])
def index():
    reg_form = RegistrationForm() # custom form we created

    #* will return TRUE if VALID form was submitted using the POST method
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
    
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted into DB! "

    return render_template('index.html', form=reg_form)


if __name__ == "__main__":
    app.run(debug=True)