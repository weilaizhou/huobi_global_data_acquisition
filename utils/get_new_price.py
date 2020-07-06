import __init__


def get_new_price(coin_type):
    '''获取最新价格
    Agrs:
        coin_type: 网址的get参数，传入格式为 NAME/NAME
    '''
    # 处理参数  NAME/NAME -> namename
    coin_type_dispose = __init__.coin_type_dispose(coin_type, '/', '')
    # 获取返回结果
    get_new_price_url = __init__.get_new_price_url % (coin_type_dispose)
    get_new_price_content = __init__.get_url(get_new_price_url, 'get')
    if get_new_price_content == {} or 'tick' in get_new_price_content is False:
        print('获取最新价格:%s最新价格获取失败' % (coin_type))
        return None
    # 储存和发布
    if __init__.DATABASE_TYPE == 'redis':
        get_new_price_redis(coin_type, get_new_price_content)
    elif __init__.DATABASE_TYPE == 'mysql':
        get_new_price_mysql(get_new_price_content)
    else:
        print('获取最新价格:数据存储类型错误')


def get_new_price_redis(coin_type, data):
    '''将数据存储到redis
    Agrs:
        coin_type: 货币类型
        data: 已整理数据，字典类型
    '''
    from config import redis_conn
    try:
        风控_number = float(redis_conn.REDIS['%s%s' % (__init__.风控_KEY, coin_type)].decode()) if (__init__.使用风控 is True) else 0
    except BaseException:
        风控_number = 0
    # 存储
    if __init__.推送_通道_最新价 != '':
        redis_conn.REDIS.publish(__init__.推送_通道_最新价, data['tick']['close'] + 风控_number)
    if __init__.推送_合约_最新价 != '':
        redis_conn.REDIS.set(__init__.推送_合约_最新价 % (coin_type), data['tick']['close'] + 风控_number)


def get_new_price_mysql(data):
    pass
