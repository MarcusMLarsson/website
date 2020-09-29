from flask import Blueprint, render_template, session, abort
app_file1 = Blueprint('app_file1', __name__)

# @app_file1 is the decorator
# Route URL
@app_file1.route("/")
def home():
    return render_template('home.html', token="")


if __name__ == '__index__':
    app_file1.run()
