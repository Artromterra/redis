import pickle
import redis
import json

client = redis.Redis(host='redis', port=6379)

cache = {0: 0, 1: 1}

def fibo(n):
    if n in cache:
        return cache[n]
    else:
        f = fibo(n-1) + fibo(n-2)
        cache[n] = f
        return f

def foo(number):

    cache_dict = client.get('cache_fi')
    if cache_dict:
        # return cache_dict
        decod = cache_dict.decode("utf-8")
        jdict = json.loads(decod)
        if str(number) in jdict:
            return f'из кэша: {jdict[str(number)]}'

    if number > 500:
        step = 500
        k = 100
    else:
        step = 10
        k = 1
    cache_list = [x*k+(step*(x-1)) for x in range(1, round(number/step)+1)]
    cache_list.append(number)
    fibo_list = [fibo(n) for n in cache_list]
    if cache_dict:
        jdict = json.loads(cache_dict.decode("utf-8"))
        jdict[str(number)] = str(fibo_list[-1])
        client.set('cache_fi', str(json.dumps(jdict)))
    else:
        client.set('cache_fi', str(json.dumps({str(number): str(fibo_list[-1])})))
    return f'посчитали: {fibo_list[-1]}<br><br>кэш: {str(cache_dict)}'