import json
from pymemcache.client.base import Client
import redis

def json_serializer(key, value):
    if type(value) == str:
        return value, 1
    return json.dumps(value), 2

def json_deserializer(key, value, flags):
   if flags == 1:
       return value.decode("utf-8")
   if flags == 2:
       return json.loads(value.decode("utf-8"))
   raise Exception("Unknown serialization format")

# client = Client(('localhost', 11211), serializer=json_serializer,
#                 deserializer=json_deserializer)

client = redis.Redis(host='redis', port=6379)

cache = client.get('cache')
if not cache:
    cache = {'0': 0, '1': 1}
    client.set('cache', cache)

def fibo(n):
    if str(n) in cache:
        return cache[str(n)]
    else:
        f = fibo(n-1) + fibo(n-2)
        cache[str(n)] = f
        client.set('cache', cache)
        return f

def foo(number):

    pref = 'очистить кэш: /rm<br>если ошибка - значит кэш переполнен<br><br>'
    if str(number) in cache:
        return f'{pref}из кэша: {cache[str(number)]}'
    else:
        if number > 500:
            step = 500
            k = 100
        else:
            step = 10
            k = 1
        cache_list = [x*k+(step*(x-1)) for x in range(1, round(number/step)+1)]
        cache_list.append(number)
        fibo_list = [fibo(n) for n in cache_list]
        return f'{pref}посчитали: {fibo_list[-1]}'

def boo():
    client.set('cache', {'0': 0, '1': 1})
    return 'теперь в кэше только значения для 0 и 1'