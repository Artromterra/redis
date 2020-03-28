import json
import redis

client = redis.Redis(host='redis', port=6379)

cache = client.hgetall('cache')
if not cache:
    cache = {'0': 0, '1': 1}
    client.hmset('cache', cache)

def fibo(n):
    if str(n) in cache:
        return cache[str(n)]
    else:
        f = fibo(n-1) + fibo(n-2)
        cache[str(n)] = f
        client.hmset('cache', cache)
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