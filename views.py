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

    cache_dict = client.hgetall('cache_dict')
    if cache_dict and str(number) in cache_dict:
        return f'из кэша: {cache_dict[str(number)]}'
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
        if cache_dict:
            cache_dict[str(number)] = str(fibo_list[-1])
            client.hset('cache_dict', 'r', cache_dict)
        else:
            client.hset('cache_dict', 'r', {str(number): str(fibo_list[-1])})
        return f'посчитали: {fibo_list[-1]}<br><br>кэш: {str(cache_dict)}'