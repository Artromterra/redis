import json
import redis
import pickle

def get_dict_data_from_redis(redis_client, key):
    data = redis_client.get(key)
    if data:
       try:
          return pickle.loads(data)
       except:
          return None
    return {}
    
client = redis.Redis(host='redis', port=6379)

cache = get_dict_data_from_redis(client, 'cache')
if not cache:
    cache = {'0': 0, '1': 1}
    client.set('cache', pickle.dumps(cache))

def fibo(n):
    if str(n) in cache:
        return cache[str(n)]
    else:
        f = fibo(n-1) + fibo(n-2)
        cache[str(n)] = f
        client.set('cache', pickle.dumps(cache))
        return f

def foo(number):

    pref = 'если ошибка - значит кэш переполнен<br><br>'
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