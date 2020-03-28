import redis

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

    rcache = client.hgetall('rcache')
    if rcache and str(number) in rcache:
        return f'из кэша: {rcache[str(number)]}'
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
        if rcache:
            rcache[str(number)] = fibo_list[-1]
            client.hmset('rcache', rcache)
        else:
            client.hmset('rcache', {str(number): fibo_list[-1]})
        return f'посчитали: {fibo_list[-1]}<br>{str(rcache)}'