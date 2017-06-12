#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

from tornado import web
from tornado import websocket
from tornado.options import options

from .storage import RedisStorage
from .storage import Storage


class IndexHandler(web.RequestHandler):
    def get(self, path):
        self.render(os.path.join(os.getcwd(), options.template_dir, "index.html"),
                    wsurl=options.ws_url)


class WebSocketHandler(websocket.WebSocketHandler):
    _sockets = list()
    _push_count = None
    _storage = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__class__._sockets.append(self)

        if self.__class__._storage is not None:
            pass
        elif options.redis_address:
            self.__class__._storage = Storage(RedisStorage(options.redis_address,
                                                           options.redis_key))
        else:
            self.__class__._storage = Storage()

        if self.__class__._push_count is None:
            self.__class__._push_count = self.__class__._storage.get()

    def increment_push_count(self):
        self.__class__._push_count += 1
        self.__class__._storage.set(self.__class__._push_count)
        self.wall(True)

    def do_response(self, status):
        self.write_message(bytes(json.dumps({"count": self.__class__._push_count,
                                             "clients": len(self.__class__._sockets),
                                             "message": status}),
                                 encoding="utf-8"))

    def wall(self, move=True):
        self.__class__._sockets = [x for x in self.__class__._sockets
                                   if x.ws_connection is not None]
        for x in self.__class__._sockets:
            try:
                if not move:
                    x.do_response("pole")
                elif self != x:
                    x.do_response("ping")
                else:
                    x.do_response("pong")
            except:
                pass

    def check_origin(self, origin):
        if not options.check_origin or len(origin) == 0 or origin == options.origin:
            return True
        super().check_origin(origin)

    def open(self):
        self.wall(False)

    def on_close(self):
        self.wall(False)

    def on_message(self, message):
        self.increment_push_count()
