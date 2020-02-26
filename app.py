import flask
from views import home

app = flask.Flask(__name__)
app.register_blueprint(home.blueprint)

if __name__ == '__main__':
    app.run()
