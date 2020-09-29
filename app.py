from flask import Flask, render_template, url_for, request
from home import app_file1
from blueprints.oil import app_file2


app = Flask(__name__)

app.register_blueprint(app_file1)
app.register_blueprint(app_file2)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)