# -*- coding: utf-8 -*-
import logging

from redis import Redis
from redis.exceptions import ConnectionError, TimeoutError
import simplejson as json


def cache_retry(func):
    def decorate(*args, **kargs):
        retry_times = 2
        while retry_times != 0:
            retry_times -= 1
            self = args[0]
            try:
                return func(*args, **kargs)
            except (ConnectionError, TimeoutError) as err:
                logging.warn("execute faild: %s" % err)
                self.__init__(self.host, self.port, self.db, self.password)
        logging.warn("failed to connect to redis")

    return decorate


class Cache(Redis):
    def __init__(self, host, port, db, password):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        super(Cache, self).__init__(host=self.host, port=self.port, db=self.db, password=self.password)

    @cache_retry
    def get(self, key, **kwargs):
        data_format = kwargs.pop('format', 'str')
        value = super(Cache, self).get(key)
        if data_format == 'json':
            value = json.loads(value) if value else {}
        return value

    @cache_retry
    def get_json(self, key, **kwargs):
        value = super(Cache, self).get(key)
        value = json.loads(value) if value is not None else None
        return value

    @cache_retry
    def set(self, key, value, **kwargs):
        data_format = kwargs.pop('format', 'str')
        if data_format == 'json':
            value = json.dumps(value)
        return super(Cache, self).set(key, value, **kwargs)

    @cache_retry
    def delete(self, *args):
        return super(Cache, self).delete(*args)

    @cache_retry
    def expire(self, key, time):
        return super(Cache, self).expire(key, time)
