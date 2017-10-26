# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 18:14:17 2017

@author: richard
"""
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flaskr import app



http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
IOLoop.instance().start()