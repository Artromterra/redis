from views import foo, boo
from flask import Flask

app = Flask(__name__)

@app.route('/', methods = ['GET'])
@app.route('/<int:number>', methods = ['GET'])
def show_post(number=1):
    return foo(number)