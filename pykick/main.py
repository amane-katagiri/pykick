#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
from urllib.parse import urlparse
from urllib.parse import urlunparse

from tornado import httpserver
from tornado import ioloop
from tornado import web
from tornado.options import define
from tornado.options import options

from .handler import IndexHandler
from .handler import WebSocketHandler

define("host", default="localhost")
define("port", default=8000, type=int)
define("ssl_key", default="")
define("ssl_crt", default="")
define("check_origin", default=False, type=bool)
define("origin", default="")
define("ws_url", default="ws://localhost:8000/ws")
define("template_dir", default="templates")
define("static_dir", default="static")
define("redis_address", default="")
define("redis_key", default="push_count")


def main():
    if os.path.isfile("config/server.conf"):
        options.parse_config_file("config/server.conf")
    else:
        logging.warning("server.conf is not found.")
    options.parse_command_line()

    url = urlparse(options.ws_url)
    if options.origin:
        pass
    elif url.scheme == "wss":
        options.origin = urlunparse(("https", url.netloc, "", "", "", ""))
    else:
        options.origin = urlunparse(("http", url.netloc, "", "", "", ""))

    app = web.Application([
        (urlparse(options.ws_url).path, WebSocketHandler),
        (r"/(index\.html)?", IndexHandler),
        (r"/(.*)", web.StaticFileHandler, {"path": os.path.join(os.getcwd(), options.static_dir)}),
    ])
    if options.ssl_key:
        server = httpserver.HTTPServer(app, ssl_options={
            "certfile": options.ssl_crt,
            "keyfile": options.ssl_key,
        })
    else:
        server = httpserver.HTTPServer(app)

    server.listen(options.port)
    ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
