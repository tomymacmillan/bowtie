# -*- coding: utf-8 -*-

from collections import namedtuple

from inspect import stack

from flask_socketio import emit

from uuid import uuid4

from future.utils import with_metaclass

from eventlet.event import Event


def make_event(event):

    @property
    def actualevent(self):
        name = event.__name__[3:]
        return '{uuid}#{event}'.format(uuid=self._uuid, event=name)

    actualevent.__doc__ = event.__doc__

    return actualevent


def is_event(attribute):
    return attribute.startswith('on_')


class _EventMeta(type):
    def __new__(cls, name, parents, dct):
        for k in dct:
            if is_event(k):
                dct[k] = make_event(dct[k])
        return super(_EventMeta, cls).__new__(cls, name, parents, dct)


class Component(with_metaclass(_EventMeta, object)):

    def __init__(self):
        self._uuid = id(self)

    def get(self, block=True, timeout=None):
        # queue = self._get_queue()
        # def getting():
        #     valx = queue.get(block=block, timeout=10)
        #     print('spwaned', valx)
        #     return valx
        event = Event()
        # def ack(data):
        #     print('acknowledged')
        #     print(data)
        #     # valx = queue.put(data)
        #     event.send(data)
        emit('{}#get'.format(self._uuid), callback=lambda x: event.send(x))
        # print('wait get')
        # val = [1]
        # valx = queue.get(block=block, timeout=10)
        return event.wait()
        # eventlet.spawn(getting)
        #
        # eventlet.sleep(1)
        # print(valx)
        # print('done get', valx)
        # return valx