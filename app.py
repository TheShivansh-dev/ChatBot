from flask import Flask


app = Flask(__name__)


@app.route('/')
def helloworld():
    return "grey word"

if __name__ == "__main__":
    app.run()