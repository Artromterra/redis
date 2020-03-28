from views import foo, boo
from flask import Flask

app = Flask(__name__)

# def get_hit_count():
#     retries = 5
#     while True:
#         try:
#             return cache.incr('hits')
#         except redis.exceptions.ConnectionError as exc:
#             if retries == 0:
#                 raise exc
#             retries -= 1
#             time.sleep(0.5)
@app.route('/', methods = ['GET'])
@app.route('/<int:number>', methods = ['GET'])
def show_post(number=1):
    # return 'number %d' % number
    return foo(number)

@app.route('/rm', methods = ['GET'])
def rm():
    return boo()