#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import redis


class Storage(object):
    def __init__(self, *storages):
        self.storages = storages + (NullStorage(), )
        self.iter = iter(self.storages)
        self._cur = next(self.iter)

    def next(self):
        self._cur = next(self.iter)
        logging.warning("Fall back to '{}' storage.".format(self._cur.__class__.__name__))
        return self._cur

    def cur(self):
        return self._cur

    def get(self):
        try:
            return self.cur().get()
        except RuntimeError as ex:
            logging.warning(ex.args[0])
            self.next()
            return self.get()

    def set(self, count):
        try:
            self.cur().set(count)
        except RuntimeError as ex:
            logging.warning(ex.args[0])
            self.next()
            return self.set(count)


class RedisStorage(object):
    def __init__(self, addr, key):
        self.host = addr.split(":")[0]
        try:
            self.port = addr.split(":")[1]
        except IndexError:
            self.port = 6379
        self.key = key
        self.redis = redis.StrictRedis(host=self.host, port=self.port, db=0)

    def get(self):
        try:
            buf = self.redis.get(self.key)
            if buf is not None:
                return int(buf)
            else:
                return 0
        except TypeError:
            msg = "Redis: value '{}' is invalid ({})."
            raise RuntimeError(msg.format(self.key, self.redis.get(self.key)))
        except redis.exceptions.ConnectionError:
            raise RuntimeError("Redis: connection {}:{} is invalid.".format(self.host, self.port))

    def set(self, count):
        try:
            self.redis.set(self.key, count)
        except redis.exceptions.ConnectionError:
            raise RuntimeError("Redis: connection {}:{} is invalid.".format(self.host, self.port))


class NullStorage(object):
    def get(self):
        return 0

    def set(self, count):
        logging.debug("count: {}".format(count))
