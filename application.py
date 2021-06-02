from  flask import Flask, render_template
from wtform_fields import *

app = Flask(__name__)
app.secret_key = 'replace later'

@app.route("/", methods = ["GET", "POST"])
def index():
    reg_form = RegistrationForm() # custom form we created

    #* will return TRUE if VALID form was submitted using the POST method
    if reg_form.validate_on_submit():
        return "success!!"
    return render_template('index.html', form=reg_form)

if __name__ == "__main__":
    app.run(debug=True)