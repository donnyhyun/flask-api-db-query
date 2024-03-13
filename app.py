from flask import Flask
from src.authentication import auth_app
from src.catalog import cat_app
from src.quests import quest_app


app = Flask(__name__)
app.json.sort_keys = False
app.register_blueprint(auth_app)
app.register_blueprint(cat_app)
app.register_blueprint(quest_app)


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(port=5000)
