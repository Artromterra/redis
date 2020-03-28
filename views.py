import json
import redis

client = redis.Redis(host='redis', port=6379)

# cache = client.hgetall('fibocache')
# if not cache:
#     cache = {'0': 0, '1': 1}
#     client.hmset('fibocache', cache)

cache = {'0': 0, '1': 1}

def fibo(n):
    if n in cache:
        return cache[n]
    else:
        f = fibo(n-1) + fibo(n-2)
        cache[n] = f
        # client.hmset('fibocache', cache)
        return f

def foo(number):

    # pref = 'если ошибка - значит кэш переполнен<br><br>'
    f = client.get('fibo_cache')
    if f:
        return f'из кэша: {f}'
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
        client.set('fibo_cache', fibo_list[-1])
        return f'посчитали: {fibo_list[-1]}'